# Data licences

The MIT licence in [LICENSE](LICENSE) covers the code in this repository only.

The connectome reconstructions are not ours, they are the reason any of this is
possible, and they carry their own terms. **Neither is redistributed here** —
both are downloaded by the import scripts, with file checksums recorded in
`data/*/source.lock.json`.

## MaleCNS v1.0

The complete central nervous system of a male *Drosophila melanogaster*, used
throughout this repository as the primary dataset.

- Janelia Research Campus FlyEM, MRC Laboratory of Molecular Biology,
  University of Cambridge, and Google Research
- **CC-BY 4.0**
- https://male-cns.janelia.org/
- Fetched by `src/import_graph.py` from
  `gs://flyem-male-cns/v1.0/connectome-data/flat-connectome/`

## FlyWire FAFB 783

The adult female brain, used here only to replicate published results on the
dataset they were published on.

- The FlyWire Consortium, Princeton University
- **CC-BY 4.0**
- https://flywire.ai/
- Fetched by `src/import_flywire_shiu.py`, as redistributed with
  github.com/philshiu/Drosophila_brain_model, whose model that script
  replicates

## FlyWire community annotations

Cell types, super-classes, transmitter predictions and soma positions.

- flyconnectome/flywire_annotations
- **CC-BY 4.0**
- https://github.com/flyconnectome/flywire_annotations

## Published model parameters

Most physiological constants in `src/params.py` are taken from Shiu, Sterne
et al., *Nature* 634:210-219 (2024), and from the accompanying implementation
at github.com/philshiu/Drosophila_brain_model (MIT). Each constant carries the
citation that paper gives for it, including where that citation turned out to
be a software paper or a larval preparation rather than an adult measurement.
