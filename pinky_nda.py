from pipeline import reso,stack
from stimulus import stimulus

"""
schema classes and methods
"""
import numpy as np
import datajoint as dj

schema = dj.schema('microns_L23_nda', create_tables=True)
schema.spawn_missing_classes()


@schema
class Scan(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # Information on completed scan
    session              : smallint                     # Session ID
    scan_idx             : smallint                     # Scan ID
    ---
    nframes              : int                          # number of frames per scan
    nfields              : tinyint                      # number of fields per scan
    fps                  : float                        # frames per second (Hz)
    """
    
    scan_keys = [{'animal_id': 8973, 'session': 1, 'scan_idx': 2},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 3},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 4},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 5},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 6},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 9},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 10},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 11},
                 {'animal_id': 8973, 'session': 1, 'scan_idx': 12}]
        
    @property
    def key_source(self):
        return (reso.ScanInfo & self.scan_keys).proj('nframes','nfields','fps')
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)


@schema
class Field(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # Individual fields of scans
    -> Scan
    field                : smallint                     # Field Number
    ---
    px_width             : smallint                     # field pixels per line
    px_height            : smallint                     # lines per field
    um_width             : float                        # field width (microns)
    um_height            : float                        # field height (microns)
    field_x              : float                        # field x motor coordinates (microns)
    field_y              : float                        # field y motor coordinates (microns)
    field_z              : float                        # field z motor coordinates (microns)
    """
      
    @property
    def key_source(self):
        return ((reso.ScanInfo & Scan.proj() & {'animal_id':8973}) * \
                    reso.ScanInfo.Field).proj('px_width','px_height','um_width','um_height',
                                              field_x='x',field_y='y',field_z='z')
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)
        
        
# @schema
# class RawManualPupil(dj.Manual):
#     """
#     Class methods not available outside of BCM pipeline environment
#     """
#     definition = """
#     # Pupil traces
#     -> Scan
#     ---
#     pupil_min_r          : longblob                     # vector of pupil minor radii  (pixels)
#     pupil_maj_r          : longblob                     # vector of pupil major radii  (pixels)
#     pupil_x              : longblob                     # vector of pupil x positions  (pixels)
#     pupil_y              : longblob                     # vector of pupil y positions  (pixels)
#     pupil_times          : longblob                     # vector of times relative to scan start (seconds)
#     """
    

# @schema
# class ManualPupil(dj.Manual):
#     definition = """
#     # Pupil traces
#     -> RawManualPupil
#     ---
#     pupil_min_r          : longblob                     # vector of pupil minor radii synchronized with field 1 frame times (pixels)
#     pupil_maj_r          : longblob                     # vector of pupil major radii synchronized with field 1 frame times (pixels)
#     pupil_x              : longblob                     # vector of pupil x positions synchronized with field 1 frame times (pixels)
#     pupil_y              : longblob                     # vector of pupil y positions synchronized with field 1 frame times (pixels)
#     """

# @schema
# class RawTreadmill(dj.Manual):
#     """
#     Class methods not available outside of BCM pipeline environment
#     """
#     definition = """
#     # Treadmill traces
#     ->Scan
#     ---
#     treadmill_velocity      : longblob                     # vector of treadmill velocities (cm/s)
#     treadmill_timestamps    : longblob                     # vector of times relative to scan start (seconds)
#     """

# @schema
# class Treadmill(dj.Manual):
#     """
#     Class methods not available outside of BCM pipeline environment
#     """
#     definition = """
#     # Treadmill traces
#     ->RawTreadmill
#     ---
#     treadmill_speed      : longblob                     # vector of treadmill velocities synchronized with field 1 frame times (cm/s)
#     """
    
#     @property
#     def key_source(self):
#         return nda3.Treadmill()
    
#     @classmethod
#     def fill(cls):
#         cls.insert(cls.key_source, ignore_extra_fields=True)
        

# @schema
# class FrameTimes(dj.Manual):
#     """
#     Class methods not available outside of BCM pipeline environment
#     """
#     definition = """
#     # scan times per frame (in seconds, relative to the start of the scan)
#     ->Scan
#     ---
#     frame_times        : longblob            # stimulus frame times for field 1 of each scan, (len = nframes)
#     ndepths             : smallint           # number of imaging depths recorded for each scan
#     """

    
# @schema
# class Stimulus(dj.Manual):
#     """
#     Class methods not available outside of BCM pipeline environment
#     """
#     definition = """
#     # Stimulus presented
#     -> Scan
#     ---
#     movie                : longblob                     # stimulus images synchronized with field 1 frame times (H x W X F matrix)
#     """


# @schema
# class Trial(dj.Manual):
#     definition = """
#     # Information for each Trial
#     ->Stimulus
#     trial_idx            : smallint                     # index of trial within stimulus
#     ---
#     type                 : varchar(16)                  # type of stimulus trial
#     start_idx            : int unsigned                 # index of field 1 scan frame at start of trial
#     end_idx              : int unsigned                 # index of field 1 scan frame at end of trial
#     start_frame_time     : double                       # start time of stimulus frame relative to scan start (seconds)
#     end_frame_time       : double                       # end time of stimulus frame relative to scan start (seconds)
#     frame_times          : longblob                     # full vector of stimulus frame times relative to scan start (seconds)
#     condition_hash       : char(20)                     # 120-bit hash (The first 20 chars of MD5 in base64)
#     """

@schema
class Monet(dj.Manual):
    definition = """
    # pink noise with periods of motion and orientation
    condition_hash       : char(20)                     # 120-bit hash (The first 20 chars of MD5 in base64)
    ---
    fps                  : decimal(5,2)                 # display refresh rate
    moving_noise_version : smallint                     # algorithm version; increment when code changes
    rng_seed             : double                       # random number generate seed
    tex_ydim             : smallint                     # texture dimension (pixels) 
    tex_xdim             : smallint                     # texture dimension (pixels) 
    spatial_freq_half    : float                        # spatial frequency modulated to 50 percent (cy/deg) 
    spatial_freq_stop    : float                        # spatial lowpass cutoff (cy/deg)
    temp_bandwidth       : float                        # temporal bandwidth of the stimulus (Hz)
    ori_on_secs          : float                        # duration of moving/oriented stimulus (seconds)
    ori_off_secs         : float                        # duration of unmoving/unoriented stimulus (seconds)
    n_dirs               : smallint                     # number of directions
    ori_bands            : tinyint                      # orientation width expressed in units of 2*pi/n_dirs
    ori_modulation       : float                        # mixin-coefficient of orientation biased noise
    speed                : float                        # (degrees/s)
    x_degrees            : float                        # degrees across x if screen were wrapped at shortest distance
    y_degrees            : float                        # degrees across y if screen were wrapped at shortest distance
    directions           : blob                         # directions in periods of motion (degrees)
    onsets               : blob                         # moving period onset times (seconds) 
    movie                : longblob                     # rendered uint8 movie (H X W X T)
    """
    
    @property
    def key_source(self):
        return stimulus.Monet & (stimulus.Trial & {'animal_id':8973} & Scan)

    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)

        
@schema
class MeanIntensity(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # mean intensity of imaging field over time
    ->Field
    ---
    intensities    : longblob                     # mean intensity
    """
    
    @property
    def key_source(self):
        return reso.Quality.MeanIntensity & {'animal_id':8973,'channel':1} & Scan
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)
        
        
        

@schema
class SummaryImages(dj.Manual):
    definition = """
    ->Field
    channel        : tinyint                      # green (1) or red (2) channel
    ---
    correlation    : longblob                     # average image
    average        : longblob                     # correlation image
    """
    
    @property
    def key_source(self):
        return reso.SummaryImages.Correlation.proj(correlation='correlation_image') * \
               reso.SummaryImages.Average.proj(average='average_image') & {'animal_id': 8973} & Scan
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)

@schema
class Stack(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # all slices of each stack after corrections.
    stack_session        : smallint                     # session index for the mouse
    stack_idx            : smallint                     # id of the stack
    ---
    motor_z              : float                        # (um) center of volume in the motor coordinate system (cortex is at 0)
    motor_y              : float                        # (um) center of volume in the motor coordinate system
    motor_x              : float                        # (um) center of volume in the motor coordinate system
    px_depth             : smallint                     # number of slices
    px_height            : smallint                     # lines per frame
    px_width             : smallint                     # pixels per line
    um_depth             : float                        # depth in microns
    um_height            : float                        # height in microns
    um_width             : float                        # width in microns
    surf_z               : float                        # (um) depth of first slice - half a z step (cortex is at z=0)
    """
    
    stack_key = {'animal_id':8973, 'stack_session':1, 'stack_idx':1}
    
    @property
    def key_source(self):
        fetch_str = stack.CorrectedStack.heading.dependent_attributes[3:]
        return stack.CorrectedStack.proj(*fetch_str,motor_x='x',motor_y='y',motor_z='z',
                                          stack_session='session') & self.stack_key
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)


@schema
class Registration(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # align a 2-d scan field to a stack with affine matrix learned via gradient ascent
    ->Stack
    ->Field
    ---
    a11                  : float                        # (um) element in row 1, column 1 of the affine matrix
    a21                  : float                        # (um) element in row 2, column 1 of the affine matrix
    a31                  : float                        # (um) element in row 3, column 1 of the affine matrix
    a12                  : float                        # (um) element in row 1, column 2 of the affine matrix
    a22                  : float                        # (um) element in row 2, column 2 of the affine matrix
    a32                  : float                        # (um) element in row 3, column 2 of the affine matrix
    reg_x                : float                        # z translation (microns)
    reg_y                : float                        # y translation (microns)
    reg_z                : float                        # z translation (microns)
    score                : float                        # cross-correlation score (-1 to 1)
    reg_field            : longblob                     # extracted field from the stack in the specified position
    """
    
    @property
    def key_source(self):
        fetch_str = stack.Registration.Affine.heading.dependent_attributes
        return stack.Registration.Affine.proj(*fetch_str,session='scan_session') & {'animal_id':8973} & Stack & Field
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)

# @schema
# class Coregistration(dj.Manual):
#     """
#     Class methods not available outside of BCM pipeline environment
#     """
#     definition = """
#     # transformation solutions between 2P stack and EM stack and vice versa from the Allen Institute
#     ->Stack
#     transform_id            : int                          # id of the transform
#     ---
#     version                 : varchar(256)                 # coordinate framework
#     direction               : varchar(16)                  # direction of the transform (EMTP: EM -> 2P, TPEM: 2P -> EM)
#     transform_type          : varchar(16)                  # linear (more rigid) or spline (more nonrigid)
#     transform_args=null     : longblob                     # parameters of the transform
#     transform_solution=null : longblob                     # transform solution
#     """
    
#     @property
#     def key_source(self):
#         return m65p3.Coregistration()
    
#     @classmethod
#     def fill(cls):
#         cls.insert(cls.key_source, ignore_extra_fields=True)



@schema
class Segmentation(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # Different mask segmentations
    ->Field
    mask_id         :  smallint
    ---
    pixels          : longblob      # indices into the image in column major (Fortran) order
    weights         : longblob      # weights of the mask at the indices above
    """
    
    segmentation_key = {'animal_id': 8973, 'segmentation_method': 6}

    @property
    def key_source(self):
        return reso.Segmentation.Mask & self.segmentation_key & Field

    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)


@schema
class Fluorescence(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # fluorescence traces before spike extraction or filtering
    -> Segmentation
    ---
    trace                   : longblob #fluorescence trace 
    """
    
    segmentation_key = {'animal_id': 8973, 'segmentation_method': 6}

    @property
    def key_source(self):
        return reso.Fluorescence.Trace & self.segmentation_key & Field
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)


@schema
class ScanUnit(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # single unit in the scan
    -> Scan
    unit_id                 : int               # unique per scan
    ---
    -> Fluorescence
    um_x                : smallint      # centroid x motor coordinates (microns)
    um_y                : smallint      # centroid y motor coordinates (microns)
    um_z                : smallint      # centroid z motor coordinates (microns)
    px_x                : smallint      # centroid x pixel coordinate in field (pixels
    px_y                : smallint      # centroid y pixel coordinate in field (pixels
    ms_delay            : smallint      # delay from start of frame (field 1 pixel 1) to recording ot his unit (milliseconds)
    """
    
    segmentation_key = {'animal_id': 8973, 'segmentation_method': 6}

    
    @property
    def key_source(self):
        return (reso.ScanSet.Unit * reso.ScanSet.UnitInfo) & self.segmentation_key & Field  
    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)

@schema
class Activity(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # activity inferred from fluorescence traces
    -> ScanUnit
    ---
    trace                   : longblob  #spike trace
    """
    
    segmentation_key = {'animal_id': 8973, 'segmentation_method': 6, 'spike_method': 5}

    @property
    def key_source(self):
        return reso.Activity.Trace & self.segmentation_key & Field

    
    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)

@schema
class StackUnit(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # centroids of each unit in stack coordinate system using affine registration
    -> Registration
    -> ScanUnit
    ---
    motor_x            : float    # centroid x stack coordinates with motor offset (microns)
    motor_y            : float    # centroid y stack coordinates with motor offset (microns)
    motor_z            : float    # centroid z stack coordinates with motor offset (microns)
    stack_x            : float    # centroid x stack coordinates (microns)
    stack_y            : float    # centroid y stack coordinates (microns)
    stack_z            : float    # centroid z stack coordinates (microns)
    """
    
    segmentation_key = {'animal_id': 8973, 'segmentation_method': 6}
    
    @property
    def key_source(self):
        return reso.StackCoordinates.UnitInfo & self.segmentation_key & Stack.proj() & Field

    
    @classmethod
    def fill(cls):
        stack_unit = (cls.key_source*Stack).proj(stack_x = 'round(stack_x - motor_x + um_width/2, 2)', 
                                                 stack_y = 'round(stack_y - motor_y + um_height/2, 2)', 
                                                 stack_z = 'round(stack_z - motor_z + um_depth/2, 2)')
        cls.insert((cls.key_source.proj(motor_x='stack_x', 
                                        motor_y='stack_y', 
                                        motor_z='stack_z') * stack_unit), ignore_extra_fields=True)

# @schema 
# class AreaMembership(dj.Manual):
#     definition = """
#     -> ScanUnit
#     ---
#     brain_area          : char(10)    # Visual area membership of unit
    
#     """

@schema
class MaskClassification(dj.Manual):
    """
    Class methods not available outside of BCM pipeline environment
    """
    definition = """
    # classification of segmented masks using CaImAn package
    ->Segmentation
    ---
    mask_type                 : varchar(16)                  # classification of mask as soma or artifact
    """

    @property
    def key_source(self):
        return reso.MaskClassification.Type.proj(mask_type='type') & {'animal_id': 8973, 'segmentation_method': 6} & Scan

    @classmethod
    def fill(cls):
        cls.insert(cls.key_source, ignore_extra_fields=True)


# @schema
# class Oracle(dj.Manual):
#     """
#     Class methods not available outside of BCM pipeline environment
#     """
#     definition = """
#     # Leave-one-out correlation for repeated videos in stimulus.
#     -> ScanUnit
#     ---
#     trials               : int                          # number of trials used
#     pearson              : float                        # per unit oracle pearson correlation over all movies
#     """
#     segmentation_key = {'animal_id': 17797, 'segmentation_method': 6, 'spike_method': 5}
    
#     @property
#     def key_source(self):
#         return tune.MovieOracle.Total & self.segmentation_key & nda.Field
    
#     @classmethod
#     def fill(cls):
#         cls.insert(cls.key_source, ignore_extra_fields=True)

