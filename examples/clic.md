# Using the Key4hep-Stack for CLIC Simulation and Reconstruction


This assumes that you have access to an installation of the Key4hep-stack, either via ``CVMFS`` or ``spack install``.

These commands will explain how one can run the CLIC detector simulation and reconstruction using the Key4hep-Stack.
First we will obtain all the necessary steering and input files for CLIC, simulate a few events and run the
reconstruction both with ``Marlin`` and ``k4run``. These steps can be adapted to simulate or run other ``Marlin``
processors as well.

The ``CLICPerformance`` repository contains the steering and input files.
```bash
git clone https://github.com/iLCSoft/CLICPerformance
cd CLICPerformance/clicConfig
```

## Simulation

Now we can already simulate a few events
```bash
ddsim --compactFile $LCGEO/CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml \
      --outputFile ttbar.slcio \
      --steeringFile clic_steer.py \
      --inputFiles ../Tests/yyxyev_000.stdhep \
      --numberOfEvents 3
```

## Reconstruction

### Reconstruction with Marlin

To run the reconstruction with ``Marlin``
```bash
Marlin clicReconstruction.xml \
       --InitDD4hep.DD4hepXMLFile=$LCGEO/CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml \
       --global.LCIOInputFiles=ttbar.slcio \
       --global.MaxRecordNumber=3
```

### Reconstruction with with Gaudi

We can convert the ``xml`` steering file to a Gaudi steering file
```bash
convertMarlinSteeringToGaudi.py clicReconstruction.xml  > clicReconstruction.py
```

Now we need to modify the ``clicReconstruction.py`` file to point to the ``ttbar.slcio`` input file, and change the
``DD4hepXMLFile`` parameter for the ``InitDD4hep`` algorithm.  In addition the two processors with the comment ``#
Config.OverlayFalse`` and ``# Config.TrackingConformal`` should be enabled by uncommenting their line in the ``algList``
at the end of the file.

```
sed ...

```

Then the reconstruction using the wrapper can be run with

```
k4run clicReconstruction.py
```
