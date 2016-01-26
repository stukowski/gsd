# Copyright (c) 2016 The Regents of the University of Michigan
# This file is part of the General Simulation Data (GSD) project, released under the BSD 2-Clause License.

""" hoomd schema reference implementation

The main package :py:mod:`gsd.hoomd` is a reference implementation of the
GSD schema ``hoomd``. It is a simple, but high performance and memory
efficient, reader and writer for the schema.
"""

import numpy
from collections import OrderedDict
import gsd.fl
import gsd
import logging

logger = logging.getLogger('gsd.hoomd')

__default_values = {};
__default_values['configuration/step'] = numpy.uint64(0);
__default_values['configuration/dimensions'] = numpy.uint8(3);
__default_values['configuration/box'] = numpy.array([1,1,1,0,0,0], dtype=numpy.float32);

class SnapshotParticleData:
    """ Store particle data chunks.

    Instances resulting from file read operations will always store per particle
    quantities in numpy arrays of the defined types. User created snapshots can
    provide input data as python lists, tuples, numpy arrays of different types,
    etc... Such input elements will be converted to the appropriate array type
    by :py:meth:`validate()` which is called when writing a frame.

    Examples:

    Attributes:
        N (int): Number of particles in the snapshot.
        types (list[str]): Names of the particle types.
        position (numpy.ndarray[float, ndim=2, mode='c']): Nx3 array defining particle position.
        orientation (numpy.ndarray[float, ndim=2, mode='c']): Nx4 array defining particle position.
        typeid (numpy.ndarray[uint32, ndim=1, mode='c']): N length array defining particle type ids.
        mass (numpy.ndarray[float, ndim=1, mode='c']): N length array defining particle masses.
        charge (numpy.ndarray[float, ndim=1, mode='c']): N length array defining particle charges.
        diameter (numpy.ndarray[float, ndim=1, mode='c']): N length array defining particle diameters.
        moment_inertia (numpy.ndarray[float, ndim=2, mode='c']): Nx3 array defining particle moments of inertia.
        velocity (numpy.ndarray[float, ndim=2, mode='c']): Nx3 array defining particle velocities.
        angmom (numpy.ndarray[float, ndim=2, mode='c']): Nx4 array defining particle angular momenta.
        angmom (numpy.ndarray[int32, ndim=2, mode='c']): Nx3 array defining particle images.
    """

    _default_value = OrderedDict();
    _default_value['N'] = numpy.uint32(0);
    _default_value['types'] = ['A'];
    _default_value['typeid'] = numpy.uint32(0);
    _default_value['mass'] = numpy.float32(1.0);
    _default_value['charge'] = numpy.float32(0);
    _default_value['diameter'] = numpy.float32(1.0);
    _default_value['moment_inertia'] = numpy.array([0,0,0], dtype=numpy.float32);
    _default_value['position'] = numpy.array([0,0,0], dtype=numpy.float32);
    _default_value['orientation'] = numpy.array([1,0,0,0], dtype=numpy.float32);
    _default_value['velocity'] = numpy.array([0,0,0], dtype=numpy.float32);
    _default_value['angmom'] = numpy.array([0,0,0,0], dtype=numpy.float32);
    _default_value['image'] = numpy.array([0,0,0], dtype=numpy.int32);

    def __init__(self):
        self.N = 0;
        self.position = None;
        self.orientation = None;
        self.types = None;
        self.typeid = None;
        self.mass = None;
        self.charge = None;
        self.diameter = None;
        self.moment_inertia = None;
        self.velocity = None;
        self.angmom = None;
        self.image = None;

    def validate(self):
        """ Validate all attributes.

        First, convert every per particle attribute to a numpy array of the
        proper type. Then validate that all attributes have the correct
        dimensions.

        Ignore any attributes that are ``None``.

        Warning:
            Per particle attributes that are not contiguous numpy arrays will
            be replaced with contiguous numpy arrays of the appropriate type.
        """

        logger.debug('Validating SnapshotParticleData');

        if self.position is not None:
            self.position = numpy.ascontiguousarray(self.position, dtype=numpy.float32);
            self.position = self.position.reshape([self.N, 3])
        if self.orientation is not None:
            self.orientation = numpy.ascontiguousarray(self.orientation, dtype=numpy.float32);
            self.orientation = self.orientation.reshape([self.N, 4])
        if self.typeid is not None:
            self.typeid = numpy.ascontiguousarray(self.typeid, dtype=numpy.uint32);
            self.typeid = self.typeid.reshape([self.N])
        if self.mass is not None:
            self.mass = numpy.ascontiguousarray(self.mass, dtype=numpy.float32);
            self.mass = self.mass.reshape([self.N])
        if self.charge is not None:
            self.charge = numpy.ascontiguousarray(self.charge, dtype=numpy.float32);
            self.charge = self.charge.reshape([self.N])
        if self.diameter is not None:
            self.diameter = numpy.ascontiguousarray(self.diameter, dtype=numpy.float32);
            self.diameter = self.diameter.reshape([self.N])
        if self.moment_inertia is not None:
            self.moment_inertia = numpy.ascontiguousarray(self.moment_inertia, dtype=numpy.float32);
            self.moment_inertia = self.moment_interia.reshape([self.N, 3]);
        if self.velocity is not None:
            self.velocity = numpy.ascontiguousarray(self.velocity, dtype=numpy.float32);
            self.velocity = self.velocity.reshape([self.N, 3]);
        if self.angmom is not None:
            self.angmom = numpy.ascontiguousarray(self.angmom, dtype=numpy.float32);
            self.angmom = self.angmom.reshape([self.N, 4]);
        if self.image is not None:
            self.image = numpy.ascontiguousarray(self.image, dtype=numpy.int32);
            self.image = self.image.reshape([self.N, 3]);

class Snapshot:
    """ Top level snapshot container.

    Attributes:
        particles (:py:class:`SnapshotParticleData`): Particle data snapshot.
    """

    def __init__(self):
        self.particles = SnapshotParticleData();

    def validate(self):
        """ Validate all contained snapshot data.
        """

        logger.debug('Validating Snapshot');

        self.particles.validate();

class HOOMDTrajectory:
    """ Read and/or write hoomd gsd files.

    Args:
        file (:py:class:`gsd.fl.GSDFile`): File to access.

    Create hoomd GSD files with :py:func:`create`.
    """

    def __init__(self, file):
        self.file = file;
        self._initial_frame = None;

        logger.info('opening HOOMDTrajectory: ' + self.file.name);

        if self.file.schema != 'hoomd':
            raise RuntimeError('GSD file is not a hoomd schema file: ' + self.file.name);
        if self.file.schema_version != (0,1):
            raise RuntimeError('Incompatible hoomd schema version ' + str(self.file.schema_version) + ' in: ' + self.file.name);

        logger.info('found ' + str(len(self)) + ' frames');

    def __len__(self):
        """ The number of frames in the trajectory. """
        return self.file.nframes;

    def append(self, snapshot):
        """ Append a snapshot to a hoomd gsd file.

        Args:
            snapshot (:py:class:`Snapshot`): Snapshot to append.

        Write the given snapshot to the file at the current frame and
        increase the frame counter. Do not attempt to write any fields
        that are ``None``. For all non-``None`` fields, scan them
        and see if they match the initial frame or the default value.
        If the given data differs, write it out to the frame. If it is
        the same, do not write it out as it can be instantiated either
        from the value at the initial frame or the default value.
        """

        logger.debug('Appending snapshot to hoomd trajectory: ' + self.file.name);

        snapshot.validate();

        # want the initial frame specified as a reference to detect if chunks need to be written
        if self._initial_frame is None and len(self) > 0:
            self.read_frame(0);

        for path in ['particles']:
            container = getattr(snapshot, path);
            for name in container._default_value:
                if self._should_write(path, name, snapshot):
                    logger.debug('writing data chunk: ' + path + '/' + name);
                    data = getattr(container, name);

                    if name == 'N':
                        data = numpy.array([data], dtype=numpy.uint32);
                    if name == 'types':
                        wid = max(len(w) for w in data)+1;
                        b = numpy.array(data, dtype=numpy.dtype((bytes, wid)));
                        data = b.view(dtype=numpy.int8).reshape(len(b), wid);

                    self.file.write_chunk(path + '/' + name, data)

        self.file.end_frame();

    def _should_write(self, path, name, snapshot):
        """ Test if we should write a given data chunk.

        Args:
            path (str): Path part of the data chunk.
            name (str): Name part of the data chunk.
            snapshot (:py:class:`Snapshot`): Snapshot data is from.
        Returns:
            False if the data matches that in the initial frame. False
            if the data matches all default values. True otherwise.
        """

        container = getattr(snapshot, path);
        data = getattr(container, name);

        if data is None:
            return False;

        if self._initial_frame is not None:
            initial_container = getattr(self._initial_frame, path);
            initial_data = getattr(initial_container, name);
            if numpy.all(initial_data == data):
                logger.debug('skipping data chunk, matches frame 0: ' + path + '/' + name);
                return False;

        if numpy.all(data == container._default_value[name]):
            logger.debug('skipping data chunk, default value: ' + path + '/' + name);
            return False;

        return True;

    def extend(self, iterable):
        """ Append each item of the iterable to the file.

        Args:
            iterable: An iterable object the provides :py:class:`Snapshot`
            instances. This could be another HOOMDTrajectory, a generator
            that modifies snapshots, or a simple list of snapshots.
        """

        for item in iterable:
            self.append(item);

    def read_frame(self, idx):
        """ Read the frame at the given index from the file.

        Args:
            idx (int): Frame index to read.
        Returns:
            :py:class:`Snapshot` with the frame data

        Replace any data chunks not present in the given frame with either
        data from frame 0, or initialize from default values if not in
        frame 0. Cache frame 0 data to avoid file read overhead. Return
        any default data as non-writable numpy arrays.
        """

        if idx >= len(self):
            raise IndexError;

        logger.debug('reading frame ' + str(idx) + ' from: ' + self.file.name);

        if self._initial_frame is None and idx != 0:
            self.read_frame(0);

        snap = Snapshot();
        for path in ['particles']:
            container = getattr(snap, path);
            if self._initial_frame is not None:
                initial_frame_container = getattr(snap, path);

            container.N = 0;
            if self.file.chunk_exists(frame=idx, name='particles/N'):
                N_arr = self.file.read_chunk(frame=idx, name='particles/N');
                container.N = N_arr[0];
            else:
                if self._initial_frame is not None:
                    container.N = self._initial_frame.particles.N;

            # type names
            if self.file.chunk_exists(frame=idx, name='particles/' + 'types'):
                tmp = self.file.read_chunk(frame=idx, name='particles/' + 'types');
                tmp = tmp.view(dtype=numpy.dtype((bytes, tmp.shape[1])));
                tmp = tmp.reshape([tmp.shape[0]]);
                container.types = list(a.decode('UTF-8') for a in tmp)
            else:
                if self._initial_frame is not None:
                    container.types = self._initial_frame.particles.types;
                else:
                    container.types = container._default_value['types'];

            for name in container._default_value:
                if name == 'N' or name == 'types':
                    continue;

                # per particle quantities
                if self.file.chunk_exists(frame=idx, name='particles/' + name):
                    container.__dict__[name] = self.file.read_chunk(frame=idx, name='particles/' + name);
                else:
                    if self._initial_frame is not None and self._initial_frame.particles.N == container.N:
                        # read default from initial frame
                        container.__dict__[name] = self._initial_frame.particles.__dict__[name];
                    else:
                        # initialize from default value
                        tmp = numpy.array([container._default_value[name]]);
                        s = list(tmp.shape);
                        s[0] = container.N;
                        container.__dict__[name] = numpy.resize(tmp, new_shape=s);

                    snap.particles.__dict__[name].flags.writeable = False;

        # store initial frame
        if self._initial_frame is None and idx == 0:
            self._initial_frame = snap;

        return snap;

def create(name, snapshot):
    """ Create a hoomd gsd file from the given snapshot.

    Args:
        name (str): File name.
        snapshot (:py:class:`Snapshot`): Snapshot to write to frame 0.

    .. danger::
        The file is overwritten if it already exists.
    """

    logger.info('creating hoomd gsd file: ' + name);

    gsd.fl.create(name=name, application='gsd.hoomd ' + gsd.__version__, schema='hoomd', schema_version=[0,1]);
    with gsd.fl.GSDFile(name, 'w') as f:
        traj = HOOMDTrajectory(f);
        traj.append(snapshot);