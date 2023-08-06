"""
BFOSC/G4 pipeline
"""

import os, argparse, warnings
from glob import glob

# NumPy
import numpy as np
# AstroPy
import astropy.units as u
from astropy.io import fits
from astropy.stats import mad_std
from astropy.nddata import CCDData
# ccdproc
from ccdproc import ImageFileCollection
from ccdproc.utils.slices import slice_from_string
# specutils
from specutils import Spectrum1D
# drpy
from drpy.batch import CCDDataList
from drpy.image import concatenate
from drpy.utils import imstatistics
from drpy.plotting import plot2d, plotSpectrum1D
from drpy.twodspec.longslit import (response, illumination, align, fitcoords, 
                                    transform, trace, background, profile, extract, 
                                    calibrate2d)
from drpy.twodspec.utils import invertCoordinateMap
from drpy.onedspec import dispcor, sensfunc, calibrate1d, saveSpectrum1D

from ..utils import makeDirectory, modifyHeader
from .utils import LIBRARY_PATH, login, loadLists, getMask


def pipeline(save_dir, data_dir, hdu, keywords, steps, fits_section, slit_along, 
             n_piece, sigma, index, custom_mask, exposure, airmass, extinct, standard, 
             reference, combine, keyword, isPoint, dtype, mem_limit, show, save, 
             verbose):
    """BFOSC/G4 pipeline."""
    
    # Login message
    if verbose:
        login('Grism 4')
    
    # Make directories
    if verbose:
        print('\n[MAKE DIRECTORIES]')
        print(f'  - Changing working directory to {save_dir}...')
    os.chdir(save_dir)
    fig_path = makeDirectory(parent='', child='fig', verbose=verbose)
    pro_path = makeDirectory(parent='', child='pro', verbose=verbose)
    cal_path = makeDirectory(parent='', child='cal', verbose=verbose)
    
    # Construct image file collection
    ifc = ImageFileCollection(
        location=data_dir, keywords=keywords, find_fits_by_reading=False, 
        filenames=None, glob_include='*.fit', glob_exclude=None, ext=hdu)
    
    # Modify fits header
    #   Note that image file collection is constructed before header modification.
    if 'header' in steps:
        if verbose:
            print('\n[HEADER MODIFICATION]')
        for file_name in ifc.files_filtered(include_path=True):
            modifyHeader(file_name, verbose=verbose)
    
    # Load gain and readout noise
    first_file = ifc.files_filtered(include_path=True)[0]
    gain = fits.getval(first_file, 'GAIN', ext=hdu) * u.photon / u.adu
    rdnoise = fits.getval(first_file, 'RDNOISE', ext=hdu) * u.photon
    
    if 'trim' in steps:
        custom_mask = custom_mask[slice_from_string(fits_section, fits_convention=True)]
        trim = True
    else:
        trim = False
    
    # Bias combination
    if ('bias.combine' in steps) or ('bias' in steps):
        
        if verbose:
            print('\n[BIAS COMBINATION]')
        
        # Load bias
        if verbose:
            print('  - Loading bias...')
        ifc_bias = ifc.filter(regex_match=True, imagetyp='Bias Frame')
        bias_list = CCDDataList.read(
            file_list=ifc_bias.files_filtered(include_path=True), hdu=hdu)

        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            bias_list = bias_list.trim_image(fits_section=fits_section)
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        bias_list_gain_corrected = bias_list.gain_correct(gain=gain)
        
        bias_list_gain_corrected.statistics(verbose=verbose)
        
        # Combine bias
        if verbose:
            print('  - Combining...')
        master_bias = bias_list_gain_corrected.combine(
            method='average', mem_limit=mem_limit, sigma_clip=True, 
            sigma_clip_low_thresh=3, sigma_clip_high_thresh=3, 
            sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std, 
            output_file=os.path.join(cal_path, 'master_bias.fits'), dtype=dtype, 
            overwrite_output=True)
        
        imstatistics(master_bias, verbose=verbose)
        
        # Plot master bias
        plot2d(
            master_bias.data, title='master bias', show=show, save=save, path=fig_path)
        
        # Release memory
        del bias_list

    # Flat combination
    if ('flat.combine' in steps) or ('flat' in steps):
        
        if verbose:
            print('\n[FLAT COMBINATION]')
        
        # Load flat
        if verbose:
            print('  - Loading flat...')
        ifc_flat = ifc.filter(regex_match=True, obstype='SPECLFLAT')
        flat_list = CCDDataList.read(
            file_list=ifc_flat.files_filtered(include_path=True), hdu=hdu)
        
        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            flat_list = flat_list.trim_image(fits_section=fits_section)
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        flat_list_gain_corrected = flat_list.gain_correct(gain=gain)
        
        flat_list_gain_corrected.statistics(verbose=verbose)

        # Subtract bias
        #   Uncertainties created here (equal to that of ``master_bias``) are useless!!!
        if verbose:
            print('  - Subtracting bias...')
        if 'master_bias' not in locals():
            master_bias = CCDData.read(os.path.join(cal_path, 'master_bias.fits'))
        flat_list_bias_subtracted = flat_list_gain_corrected.subtract_bias(master_bias)
        
        flat_list_bias_subtracted.statistics(verbose=verbose)

        # Combine flat
        #   Uncertainties created above are overwritten here!!!
        if verbose:
            print('  - Combining...')
        scaling_func = lambda ccd: 1 / np.ma.average(ccd)
        combined_flat = flat_list_bias_subtracted.combine(
            method='average', scale=scaling_func, mem_limit=mem_limit, sigma_clip=True, 
            sigma_clip_low_thresh=3, sigma_clip_high_thresh=3, 
            sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std, 
            output_file=os.path.join(cal_path, 'combined_flat.fits'), dtype=dtype, 
            overwrite_output=True)

        imstatistics(combined_flat, verbose=verbose)
        
        # Plot combined flat
        plot2d(
            combined_flat.data, title='combined flat', show=show, save=save, 
            path=fig_path)
        
        # Release memory
        del flat_list, flat_list_bias_subtracted

    # Response
    if ('flat.normalize.response' in steps) or \
       ('flat.normalize' in steps) or \
       ('flat' in steps):
        
        if verbose:
            print('\n[RESPONSE]')
        
        # Response calibration
        if 'combined_flat' not in locals():
            combined_flat = CCDData.read(os.path.join(cal_path, 'combined_flat.fits'))
        combined_flat.mask |= custom_mask
        reflat = response(
            ccd=combined_flat, slit_along=slit_along, n_piece=n_piece, maxiters=0, 
            sigma_lower=None, sigma_upper=None, grow=False, use_mask=True, plot=save, 
            path=fig_path)

        imstatistics(reflat, verbose=verbose)
        
        # Plot response calibrated flat
        plot2d(reflat.data, title='reflat', show=show, save=save, path=fig_path)
        
        # Plot response mask
        plot2d(
            reflat.mask.astype(int), vmin=0, vmax=1, title='response mask', show=show, 
            save=save, path=fig_path)
        
        # Write response calibrated flat to file
        reflat.write(os.path.join(cal_path, 'reflat.fits'), overwrite=True)
    
    # Illumination
    if ('flat.normalize.illumination' in steps) or \
       ('flat.normalize' in steps) or \
       ('flat' in steps):

        if verbose:
            print('\n[ILLUMINATION]')
        
        # Illumination modeling
        if 'reflat' not in locals():
            reflat = CCDData.read(os.path.join(cal_path, 'reflat.fits'))
        ilflat = illumination(
            ccd=reflat, slit_along=slit_along, method='Gaussian2D', sigma=sigma, 
            bins=10, maxiters=5, sigma_lower=3, sigma_upper=3, grow=5, use_mask=True, 
            plot=save, path=fig_path)

        imstatistics(ilflat, verbose=verbose)

        # Plot illumination
        plot2d(ilflat.data, title='illumination', show=show, save=save, path=fig_path)
        
        # Plot illumination mask
        plot2d(
            ilflat.mask.astype(int), vmin=0, vmax=1, title='illumination mask', 
            show=show, save=save, path=fig_path)
        
        # Write illumination to file
        ilflat.write(os.path.join(cal_path, 'illumination.fits'), overwrite=True)

    # Flat normalization
    if ('flat.normalize' in steps) or ('flat' in steps):
        
        if verbose:
            print('\n[FLAT NORMALIZATION]')
        
        # Normalization
        if 'reflat' not in locals():
            reflat = CCDData.read(os.path.join(cal_path, 'reflat.fits'))
        if 'ilflat' not in locals():
            ilflat = CCDData.read(os.path.join(cal_path, 'ilflat.fits'))
        normalized_flat = reflat.divide(ilflat, handle_meta='first_found')
        
        # Plot normalized flat
        plot2d(
            normalized_flat.data, title='normalized flat', show=show, save=save, 
            path=fig_path)
        
        # Plot normalized flat mask
        plot2d(
            normalized_flat.mask.astype(int), title='normalized flat mask', show=show, 
            save=save, path=fig_path)
        
        normalized_flat.mask = None
        
        # Write normalized flat to file
        normalized_flat.write(
            os.path.join(cal_path, 'normalized_flat.fits'), overwrite=True)
    
    # Lamp concatenation
    if ('lamp.concatenate' in steps) or ('lamp' in steps):
        
        if verbose:
            print('\n[LAMP CONCATENATION]')
        
        # Load lamp
        if verbose:
            print('  - Loading lamp...')
        ifc_lamp = ifc.filter(regex_match=True, obstype='SPECLLAMP')
        lamp_list = CCDDataList.read(
            file_list=ifc_lamp.files_filtered(include_path=True), hdu=hdu)

        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            lamp_list = lamp_list.trim_image(fits_section=fits_section)
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        lamp_list_gain_corrected = lamp_list.gain_correct(gain=gain)
        
        lamp_list_gain_corrected.statistics(verbose=verbose)
        
        # Subtract bias
        #   Uncertainties created here (equal to that of ``master_bias``) are useless!!!
        if verbose:
            print('  - Subtracting bias...')
        if 'master_bias' not in locals():
            master_bias = CCDData.read(os.path.join(cal_path, 'master_bias.fits'))
        lamp_list_bias_subtracted = lamp_list_gain_corrected.subtract_bias(master_bias)
        
        lamp_list_bias_subtracted.statistics(verbose=verbose)
        
        # Create real uncertainty!!!
        if verbose:
            print('  - Creating deviation...')
        lamp_list_bias_subtracted_with_deviation = (
            lamp_list_bias_subtracted.create_deviation(
                gain=None, readnoise=rdnoise, disregard_nan=True)
        )
        
        # Concatenate
        if verbose:
            print('  - Concatenating...')
        # Ensure that the first is the short exposure
        exptime = ifc_lamp.summary['exptime'].data
        if exptime[0] > exptime[1]:
            lamp_list_bias_subtracted_with_deviation = (
                lamp_list_bias_subtracted_with_deviation[::-1]
            )
        concatenated_lamp = concatenate(
            lamp_list_bias_subtracted_with_deviation, fits_section=f'[:{index}, :]', 
            scale=None)
        
        # Plot concatenated lamp
        plot2d(
            concatenated_lamp.data, title='concatenated lamp', show=show, save=save, 
            path=fig_path)
        
        # Write concatenated lamp to file
        concatenated_lamp.write(
            os.path.join(cal_path, 'concatenated_lamp.fits'), overwrite=True)
        
        # Release memory
        del (lamp_list, lamp_list_bias_subtracted, 
             lamp_list_bias_subtracted_with_deviation)
    
    # Curvature rectification
    if ('lamp.rectify' in steps) or ('lamp' in steps):
        
        if verbose:
            print('\n[CURVATURE RECTIFICATION]')
        
        # Fit coordinates
        if verbose:
            print('  - Fitting coordinates...')
        if 'concatenated_lamp' not in locals():
            concatenated_lamp = CCDData.read(
                os.path.join(cal_path, 'concatenated_lamp.fits'))
        U, _ = fitcoords(
            ccd=concatenated_lamp, slit_along=slit_along, order=1, n_med=15, n_piece=3, 
            prominence=1e-3, maxiters=3, sigma_lower=3, sigma_upper=3, grow=False, 
            use_mask=False, plot=save, path=fig_path, height=0, threshold=0, 
            distance=5, width=5, wlen=15, rel_height=1, plateau_size=1)
        
        # Invert coordinate map
        if verbose:
            print('  - Inverting coordinate map...')
        X, Y = invertCoordinateMap(slit_along, U)
        np.save(os.path.join(cal_path, 'X.npy'), X)
        np.save(os.path.join(cal_path, 'Y.npy'), Y)
        
        # Rectify curvature
        if verbose:
            print('  - Rectifying curvature...')
        transformed_lamp = transform(ccd=concatenated_lamp, X=X, Y=Y)
        
        # Plot transformed lamp
        plot2d(
            transformed_lamp.data, title='transformed lamp', show=show, save=save, 
            path=fig_path)
        
        # Write transformed lamp to file
        transformed_lamp.write(
            os.path.join(cal_path, 'transformed_lamp.fits'), overwrite=True)
    
    # Correct targets
    if ('targ' in steps):
        
        if verbose:
            print('\n[TARGET CORRECTION]')
        
        # Load targ
        if verbose:
            print('  - Loading targ...')
        ifc_targ = ifc.filter(regex_match=True, obstype='SPECLTARGET|SPECLFLUXREF')
        targ_list = CCDDataList.read(
            file_list=ifc_targ.files_filtered(include_path=True), hdu=hdu)
        
        # Trim
        if trim:
            if verbose:
                print('  - Trimming...')
            targ_list = targ_list.trim_image(fits_section=fits_section)
        
        # Correct gain
        if verbose:
            print('  - Correcting gain...')
        targ_list_gain_corrected = targ_list.gain_correct(gain=gain)
        
        targ_list_gain_corrected.statistics(verbose=verbose)
        
        # Subtract bias
        #   Uncertainties created here (equal to that of ``master_bias``) are useless!!!
        if verbose:
            print('  - Subtracting bias...')
        if 'master_bias' not in locals():
            master_bias = CCDData.read(os.path.join(cal_path, 'master_bias.fits'))
        targ_list_bias_subtracted = targ_list_gain_corrected.subtract_bias(master_bias)
        
        targ_list_bias_subtracted.statistics(verbose=verbose)

        # Create real uncertainty!!!
        if verbose:
            print('  - Creating deviation...')
        targ_list_bias_subtracted_with_deviation = (
            targ_list_bias_subtracted.create_deviation(
                gain=None, readnoise=rdnoise, disregard_nan=True)
        )
        
        # Flat-fielding
        if verbose:
            print('  - Flat-fielding...')
        if 'normalized_flat' not in locals():
            normalized_flat = CCDData.read(
                os.path.join(cal_path, 'normalized_flat.fits'))
        targ_list_flat_fielded = (
            targ_list_bias_subtracted_with_deviation.flat_correct(normalized_flat)
        )
        
        # Identify flux standard
        isStandard = ifc_targ.summary['obstype'].data == 'SPECLFLUXREF'
        # isStandard = np.array([1, 0, 0, 0], dtype=bool)
        
        if isStandard.sum() > 0:
            
            if isStandard.sum() > 1:
                raise RuntimeError('More than one standard spectrum found.')
            
            else:
                
                index_standard = np.where(isStandard)[0][0]
                
                key_standard = ifc_targ.summary['object'].data[index_standard]
                standard_flat_fielded = targ_list_flat_fielded[index_standard]
                
                # Plot
                plot2d(
                    standard_flat_fielded.data, title=f'{key_standard} flat-fielded', 
                    show=show, save=save, path=fig_path)

                # Write standard spectrum to file
                if verbose:
                    print(
                        f'  - Saving {key_standard} (standard) spectrum to '
                        f'{pro_path}...')
                standard_flat_fielded.write(
                    os.path.join(pro_path, f'{key_standard}_flat_fielded.fits'), 
                    overwrite=True)

    if ('extract' in steps) & ('standard_flat_fielded' in locals()):
        
        if verbose:
            print('\n[EXTRACTION]...')
            print(f'  - Tracing {key_standard} (standard)...')
        
        # Trace (trace the brightest spectrum)
        trace1d_standard = trace(
            ccd=standard_flat_fielded, slit_along=slit_along, fwhm=10, method='trace', 
            interval=None, n_med=10, n_piece=5, maxiters=5, sigma_lower=2, 
            sigma_upper=2, grow=False, title=key_standard, show=show, save=save, 
            path=fig_path)
        
        # Write standard trace to file (of type float64)
        saveSpectrum1D(
            os.path.join(cal_path, f'trace1d_{key_standard}.fits'), trace1d_standard, 
            overwrite=True)
        
        if verbose:
            print('  - Extracting 1-dimensional lamp spectra...')
        
        # Extract lamp spectrum for standard (of type float64)
        if 'concatenated_lamp' not in locals():
            concatenated_lamp = CCDData.read(
                os.path.join(cal_path, 'concatenated_lamp.fits'))
        lamp1d_standard = extract(
            ccd=concatenated_lamp, slit_along=slit_along, method='sum', 
            trace1d=trace1d_standard, aper_width=150, n_aper=1, 
            title=f'lamp1d for {key_standard}', show=show, save=save, path=fig_path)
        
        # Extract lamp spectrum for target (of type float64)
        if 'transformed_lamp' not in locals():
            transformed_lamp = CCDData.read(
                os.path.join(cal_path, 'transformed_lamp.fits'))
        lamp1d_target = extract(
            ccd=transformed_lamp, slit_along=slit_along, method='sum', trace1d=750, 
            aper_width=10, n_aper=1, title='lamp1d for target', show=show, save=save, 
            path=fig_path)
        
        if verbose:
            print('  - Correcting dispersion axis of lamp spectra...')
        
        # Correct dispersion of lamp spectrum for standard (of type float64)
        lamp1d_standard_calibrated = dispcor(
            spectrum1d=lamp1d_standard, reverse=True, reference=reference, n_piece=3, 
            refit=True, maxiters=5, sigma_lower=3, sigma_upper=3, grow=False, 
            use_mask=True, title=key_standard, show=show, save=save, path=fig_path)
        
        # Correct dispersion of lamp spectrum for target (of type float64)
        lamp1d_target_calibrated = dispcor(
            spectrum1d=lamp1d_target, reverse=True, reference=reference, n_piece=3, 
            refit=True, maxiters=5, sigma_lower=3, sigma_upper=3, grow=False, 
            use_mask=True, title='target', show=show, save=save, path=fig_path)
        
        if verbose:
            print(f'  - Saving calibrated lamp spectra to {cal_path}...')
        
        # Write calibrated lamp spectrum for standard to file (of type float64)
        saveSpectrum1D(
            os.path.join(cal_path, f'lamp1d_{key_standard}.fits'), 
            lamp1d_standard_calibrated, overwrite=True)
        
        # Write calibrated lamp spectrum for target to file (of type float64)
        saveSpectrum1D(
            os.path.join(cal_path, 'lamp1d_target.fits'), lamp1d_target_calibrated, 
            overwrite=True)
        
        if verbose:
            print(f'  - Modeling sky background of {key_standard} (standard)...')
        
        # Model sky background of standard
        background2d_standard = background(
            ccd=standard_flat_fielded, slit_along=slit_along, trace1d=trace1d_standard, 
            distance=200, aper_width=50, degree=0, maxiters=3, sigma_lower=4, 
            sigma_upper=4, grow=False, use_uncertainty=False, use_mask=True, 
            title=key_standard, show=show, save=save, path=fig_path)
        
        # Plot sky background of standard
        plot2d(
            background2d_standard.data, title=f'background {key_standard}', show=show, 
            save=save, path=fig_path)
        
        # Write sky background of standard to file
        background2d_standard.write(
            os.path.join(pro_path, f'background_{key_standard}.fits'), 
            overwrite=True)
        
        if verbose:
            print(
                f'  - Extracting sky background spectrum of {key_standard} '
                '(standard)...')

        # Extract sky background spectrum of standard
        sky1d_standard = extract(
            ccd=background2d_standard, slit_along=slit_along, method='sum', 
            trace1d=trace1d_standard, n_aper=1, aper_width=150, use_uncertainty=False, 
            use_mask=True, spectral_axis=lamp1d_standard_calibrated.spectral_axis, 
            show=False, save=False)
        
        # Plot sky background spectrum of standard
        plotSpectrum1D(
            sky1d_standard, title=f'sky background of {key_standard}', show=show, 
            save=save, path=fig_path)
        
        # Write sky background spectrum of standard to file (of type float64)
        saveSpectrum1D(
            os.path.join(cal_path, f'sky1d_{key_standard}.fits'), sky1d_standard, 
            overwrite=True)

        if verbose:
            print(f'  - Subtracting sky background from {key_standard} (standard)...')
        
        # Subtract sky background from standard
        standard_background_subtracted = standard_flat_fielded.subtract(
            background2d_standard, handle_meta='first_found')

        # Plot background subtracted standard
        plot2d(
            standard_background_subtracted.data, 
            title=f'background subtracted {key_standard}', show=show, save=save, 
            path=fig_path)

        # Write background subtracted standard to file
        standard_background_subtracted.write(
            os.path.join(pro_path, f'{key_standard}_background_subtracted.fits'), 
            overwrite=True)

        # Extract standard spectrum (optimal)
        if verbose:
            print(f'  - Extracting {key_standard} (standard) spectrum...')

        # Model spatial profile of standard
        profile2d_standard, _ = profile(
            ccd=standard_background_subtracted, slit_along=slit_along, 
            trace1d=trace1d_standard, profile_width=150, sigma=50, maxiters=3, 
            sigma_lower=4, sigma_upper=4, grow=False, use_mask=False, 
            title=f'{key_standard}', show=show, save=save, path=fig_path)

        # Extract
        standard1d = extract(
            ccd=standard_background_subtracted, slit_along=slit_along, 
            method='optimal', profile2d=profile2d_standard, 
            background2d=background2d_standard.data, rdnoise=rdnoise.value, maxiters=5, 
            sigma_lower=5, sigma_upper=5, grow=False, 
            spectral_axis=lamp1d_standard_calibrated.spectral_axis, 
            use_uncertainty=True, use_mask=True, title=key_standard, show=show, 
            save=save, path=fig_path)

        # Plot standard spectrum
        plotSpectrum1D(
            standard1d, title=key_standard, show=show, save=save, path=fig_path)

        # Write standard spectrum to file (of type float64)
        saveSpectrum1D(
            os.path.join(cal_path, f'{key_standard}.fits'), standard1d, 
            overwrite=True)

        if standard is not None:

            if verbose:
                print('  - Fitting sensitivity function...')
            
            # Fit sensitivity function
            sens1d, spl = sensfunc(
                spectrum1d=standard1d, exptime=exposure, airmass=airmass, 
                extinct=extinct, standard=standard, bandwid=10, bandsep=10, n_piece=19, 
                maxiters=5, sigma_lower=1, sigma_upper=3, grow=False, show=show, 
                save=save, path=fig_path)
            
            sens1d = Spectrum1D(
                spectral_axis=lamp1d_target_calibrated.spectral_axis, 
                flux=(spl(lamp1d_target_calibrated.spectral_axis.value) * sens1d.flux.unit), 
                uncertainty=sens1d.uncertainty, meta=sens1d.meta)
            
            if verbose:
                print(f'  - Saving sensitivity function to {cal_path}...')
            
            # Write sensitivity function to file (of type float64)
            saveSpectrum1D(
                os.path.join(cal_path, 'sens1d.fits'), sens1d, overwrite=True)
    
    if 'targ' in steps:
        
        # Remove flux standard
        ifc_targ = ifc_targ.filter(regex_match=True, obstype='SPECLTARGET')
        targ_list_flat_fielded = targ_list_flat_fielded[~isStandard]
        
        # Group
        ifc_targ_summary = ifc_targ.summary
        ifc_targ_summary_grouped = ifc_targ_summary.group_by(keyword)
        keys = ifc_targ_summary_grouped.groups.keys[keyword].data
        if verbose:
            print('  - Grouping')
            print(f'    - {keys.shape[0]} groups: ' + ', '.join(keys))
        
        for key in keys:
            
            if verbose:
                print(f'  - Dealing with group {key}...')
            mask = ifc_targ_summary[keyword].data == key
            
            if (mask.sum() > 1) & combine:
                
                if mask.sum() >= 3:
                
                    # Skip cosmic ray removal
                    targ_list_cosmicray_corrected = targ_list_flat_fielded[mask]
                    
                else:
                    
                    # Remove cosmic ray
                    if verbose:
                        print('    - Removing cosmic ray...')
                    targ_list_cosmicray_corrected = (
                        targ_list_flat_fielded[mask].cosmicray_lacosmic(
                            use_mask=False, gain=(1 * u.dimensionless_unscaled), 
                            readnoise=rdnoise, sigclip=4.5, sigfrac=0.3, objlim=1, 
                            niter=5, verbose=True)
                    )
                    
                # Rectify curvature
                if verbose:
                    print('    - Rectifying curvature...')
                if 'X' not in locals():
                    X = np.load(os.path.join(cal_path, 'X.npy'))
                if 'Y' not in locals():
                    Y = np.load(os.path.join(cal_path, 'Y.npy'))
                targ_list_transformed = (
                    targ_list_cosmicray_corrected.apply_over_ccd(transform, X=X, Y=Y)
                )
                    
                # Align
                if verbose:
                    print('    - Aligning...')
                targ_list_aligned = align(targ_list_transformed, slit_along, index=0)

                # Combine
                if verbose:
                    print('    - Combining...')
                exptime = ifc_targ_summary['exptime'].data[mask]
                scale = exptime.max() / exptime
                targ_combined = targ_list_aligned.combine(
                    method='average', scale=scale, mem_limit=mem_limit, 
                    sigma_clip=True, sigma_clip_low_thresh=3, sigma_clip_high_thresh=3, 
                    sigma_clip_func=np.ma.median, sigma_clip_dev_func=mad_std, 
                    output_file=os.path.join(pro_path, f'{key}_combined.fits'), 
                    dtype=dtype, overwrite_output=True)
                if verbose:
                    print(f'    - Saving combined {key} to {pro_path}...')
                
                # Plot
                plot2d(
                    targ_combined.data, title=f'combined {key}', show=show, save=save, 
                    path=fig_path)
                
                if not isPoint:
                    
                    # Calibrate
                    if verbose:
                        print(f'    - Calibrating combined {key}...')
                    targ_calibrated = calibrate2d(
                        ccd=targ_combined, slit_along=slit_along, exptime=exposure, 
                        airmass=airmass, extinct=extinct, sens1d=sens1d, 
                        use_uncertainty=False)

                    # Write calibrated spectrum to file
                    if verbose:
                        print(f'    - Saving calibrated {key} to {pro_path}...')
                    targ_calibrated.write(
                        os.path.join(pro_path, f'{key}_calibrated.fits'), overwrite=True)
                
                else:
                    
                    # Trace (trace the brightest spectrum)
                    if verbose:
                        print(f'    - Tracing {key} (target)...')
                    trace1d_target = trace(
                        ccd=targ_combined, slit_along=slit_along, fwhm=10, 
                        method='center', interval=None, title=f'{key}', show=show, 
                        save=save, path=fig_path)
                    shift = (
                        trace1d_standard.meta['header']['TRCENTER'] 
                        - trace1d_target.meta['header']['TRCENTER']) * u.pixel
                    trace1d_target = Spectrum1D(
                        flux=(trace1d_standard.flux - shift), meta=trace1d_target.meta)
                    
                    # Extract target spectrum (optimal)
                    if verbose:
                        print(f'    - Extracting {key} (target) spectrum...')
                    
                    # Model sky background of target
                    background2d_target = background(
                        ccd=targ_combined, slit_along=slit_along, trace1d=trace1d_target, 
                        distance=100, aper_width=50, degree=0, maxiters=3, sigma_lower=4, 
                        sigma_upper=4, grow=False, use_uncertainty=False, use_mask=True, 
                        title=key, show=show, save=save, path=fig_path)
                    
                    # Write sky background of standard to file
                    background2d_target.write(
                        os.path.join(pro_path, f'background_{key}.fits'), 
                        overwrite=True)

                    # Subtract sky background from target
                    target_background_subtracted = targ_combined.subtract(
                        background2d_target, handle_meta='first_found')
                    
                    # Plot background subtracted target
                    plot2d(
                        target_background_subtracted.data, 
                        title=f'background subtracted {key}', show=show, save=save, 
                        path=fig_path)
                    
                    # Write background subtracted target to file
                    target_background_subtracted.write(
                        os.path.join(pro_path, f'{key}_background_subtracted.fits'), 
                        overwrite=True)
                    
                    # Model spatial profile of target
                    profile2d_target, _ = profile(
                        ccd=target_background_subtracted, slit_along=slit_along, 
                        trace1d=trace1d_target, profile_width=150, sigma=50, 
                        maxiters=3, sigma_lower=4, sigma_upper=4, grow=False, 
                        use_mask=False, title=key, show=show, save=save, path=fig_path)

                    # Extract
                    target1d = extract(
                        ccd=target_background_subtracted, slit_along=slit_along, 
                        method='optimal', profile2d=profile2d_target, 
                        background2d=background2d_target.data, rdnoise=rdnoise.value, 
                        maxiters=5, sigma_lower=5, sigma_upper=5, grow=False, 
                        spectral_axis=lamp1d_target_calibrated.spectral_axis, 
                        use_uncertainty=True, use_mask=True, title=key, show=show, 
                        save=save, path=fig_path)
                    
                    # Plot target spectrum
                    plotSpectrum1D(
                        target1d, title=key, show=show, save=save, path=fig_path)
                    
                    # Write calibrated spectrum to file
                    saveSpectrum1D(
                        os.path.join(pro_path, f'{key}.fits'), target1d, 
                        overwrite=True)
                    
                    # Calibrate target spectrum
                    if verbose:
                        print(f'    - Calibrating {key}...')
                    target1d_calibrated = calibrate1d(
                        spectrum1d=target1d, exptime=exposure, airmass=airmass, 
                        extinct=extinct, sens1d=sens1d, use_uncertainty=False)
                    
                    # Plot calibrated target spectrum
                    plotSpectrum1D(
                        target1d_calibrated, title=f'calibrated {key}', show=show, 
                        save=save, path=fig_path)
                    
                    # Write calibrated spectrum to file
                    if verbose:
                        print(f'    - Saving calibrated {key} to {pro_path}...')
                    saveSpectrum1D(
                        os.path.join(pro_path, f'{key}_calibrated.fits'), 
                        target1d_calibrated, overwrite=True)
                    
            else:
                
                # Remove cosmic ray
                if verbose:
                    print('    - Removing cosmic ray...')
                targ_list_cosmicray_corrected = (
                    targ_list_flat_fielded[mask].cosmicray_lacosmic(
                        use_mask=False, gain=(1 * u.dimensionless_unscaled), 
                        readnoise=rdnoise, sigclip=4.5, sigfrac=0.3, objlim=1, 
                        niter=5, verbose=True)
                )

                # Rectify curvature
                if verbose:
                    print('    - Rectifying curvature...')
                if 'X' not in locals():
                    X = np.load(os.path.join(cal_path, 'X.npy'))
                if 'Y' not in locals():
                    Y = np.load(os.path.join(cal_path, 'Y.npy'))
                targ_list_transformed = targ_list_cosmicray_corrected.apply_over_ccd(
                        transform, X=X, Y=Y)
                
                n = int(np.log10(mask.sum())) + 1
                
                for i, targ_transformed in enumerate(targ_list_transformed):
                    
                    if mask.sum() == 1:
                        new_name = f'{key}'
                    else:
                        new_name = f'{key}_{(i + 1):0{n}d}'

                    # Plot
                    plot2d(
                        targ_transformed.data, title=f'corrected {new_name}', 
                        show=show, save=save, path=fig_path)

                    # Write transformed spectrum to file
                    if verbose:
                        print(f'    - Saving corrected {new_name} to {pro_path}...')
                    targ_transformed.write(
                        os.path.join(pro_path, f'{key}_corrected.fits'), overwrite=True)
                
                    # Calibrate                    
                    if verbose:
                        print(f'    - Calibrating corrected {new_name}...')
                    targ_calibrated = calibrate2d(
                        ccd=targ_transformed, slit_along=slit_along, exptime=exposure, 
                        airmass=airmass, extinct=extinct, sens1d=sens1d, 
                        use_uncertainty=False)
                    
                    # Write calibrated spectrum to file
                    if verbose:
                        print(f'    - Saving calibrated {new_name} to {pro_path}...')
                    targ_calibrated.write(
                        os.path.join(pro_path, f'{key}_calibrated.fits'), overwrite=True)


def main():
    """Command line tool."""
    
    # External parameters
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input_dir', required=True, type=str, 
        help='Input (data) directory.'
    )
    parser.add_argument(
        '-m', '--semester', required=True, type=str, 
        help='Observation semester.'
    )
    parser.add_argument(
        '-w', '--slit_width', required=True, type=float, choices=[1.8, 2.3], 
        help='Slit width.'
    )
    parser.add_argument(
        '-o', '--output_dir', default='', type=str, 
        help='Output (saving) directory.'
    )
    parser.add_argument(
        '-r', '--reference', default=None, type=str, 
        help='Reference spectrum for wavelength calibration.'
    )
    parser.add_argument(
        '-s', '--standard', default=None, type=str, 
        help='Path to the standard spectrum in the library.'
    )
    parser.add_argument(
        '-c', '--combine', action='store_true', 
        help='Combine or not.'
    )
    parser.add_argument(
        '-k', '--keyword', default='object', type=str, 
        help='Keyword for grouping.'
    )
    parser.add_argument(
        '-x', '--extract', action='store_true', 
        help='Extract 1-dimensional spectra or not.'
    )
    parser.add_argument(
        '-p', '--point', action='store_true', 
        help='Point source or not.'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', 
        help='Verbose or not.'
    )
        
    # Parse
    args = parser.parse_args()
    data_dir = os.path.abspath(args.input_dir)
    semester = args.semester
    slit_width = str(args.slit_width).replace('.', '')
    save_dir = os.path.abspath(args.output_dir)
    reference = args.reference
    standard = args.standard
    combine = args.combine
    keyword = args.keyword
    extract = args.extract
    isPoint = args.point
    verbose = args.verbose
    
    steps = ['header', 'trim', 'bias', 'flat', 'lamp', 'targ']

    if extract:
        steps.append('extract')

    # Internal parameters
    hdu = 0
    shape = (2048, 2048)
    slit_along = 'col'
    keywords = [
        'date-obs', 'obstype', 'object', 'ra', 'dec', 'filter', 'exptime', 'rdnoise', 
        'gain']
    
    fits_section = '[1:1900, 330:1830]'
    index = 665
    n_piece = 23
    sigma = (20, 30)
    exposure = 'EXPTIME'
    airmass = 'AIRMASS'
    extinct = 'baoextinct.dat'
    dtype = 'float32'
    show = False
    save = True
    mem_limit = 500e6
    
    # Can slit18 be used to calibrate slit23?
    if not reference:
        reference = sorted(
            glob(os.path.join(LIBRARY_PATH, f'bfosc_g4_slit{slit_width}*.fits'))))[-1]
    else:
        reference = os.path.abspath(reference)
    if not os.path.exists(reference):
        raise ValueError('Reference not found.')
    
    semester_path = os.path.join(LIBRARY_PATH, semester)
    if not os.path.exists(semester_path):
        raise ValueError('Semester not found.')
    
    region = os.path.join(semester_path, f'bfosc_g4_slit{slit_width}_{semester}.reg')
    custom_mask = getMask(region_name=region, shape=shape)
        
    # Run pipeline
    pipeline(
        save_dir=save_dir, data_dir=data_dir, hdu=hdu, keywords=keywords, 
        steps=steps, fits_section=fits_section, slit_along=slit_along, 
        n_piece=n_piece, sigma=sigma, index=index, custom_mask=custom_mask, 
        exposure=exposure, airmass=airmass, extinct=extinct, standard=standard, 
        reference=reference, combine=combine, keyword=keyword, isPoint=isPoint, 
        dtype=dtype, mem_limit=mem_limit, show=show, save=save, verbose=verbose)

if __name__ == '__main__':
        main()