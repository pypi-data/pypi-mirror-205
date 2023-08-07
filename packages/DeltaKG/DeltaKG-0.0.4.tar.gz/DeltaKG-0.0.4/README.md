# KGEditor

Code for our paper "Editing Language Model-based Knowledge Graph Embeddings".

To use as a python module
==========

```
pip install -kgeditor
```

Run the experiments
==========

## Training

### Edit Task

To train the KGEditor model in the paper on the dataset `E-FB15k237`, run the command below. For another dataset `E-WN18RR` just replacing the dataset name will be fine.

```shell
./scripts/kgeditor_fb15k237_edit.sh
```

### Add Task

To train the KGEditor model in the paper on the dataset `A-FB15k237`, run the command below. For another dataset `A-WN18RR` just replacing the dataset name will be fine.

```shell
./scripts/kgeditor_fb15k237_add.sh
```

Models
==========

This [folder](https://drive.google.com/drive/folders/1EOHdg8rC9iwgSyKl5RnEv9z6ATW5Ntbr?usp=share_link) contains the base models used for this work.
