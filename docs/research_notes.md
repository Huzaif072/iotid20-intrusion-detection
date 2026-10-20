# Research provenance and reproduction limits

Paper: Zaki, Yaseen, Imran, Kazim (2026). **Attention-Enhanced Hybrid Deep Learning for Intrusion Detection in IoT Networks**. *IET Networks* 15(1), e70037. DOI: https://doi.org/10.1049/ntw2.70037

Source dataset (cited by the paper): https://www.kaggle.com/datasets/rohulaminlabid/iotid20-dataset

Reported IoTID20: **86 raw columns**, **3 target columns** (`Label`, `Cat`, `Sub_Cat`), **83 candidate features**, approximately **625,415 records used in the paper** (500,332 training / 125,083 testing), not necessarily the same count as all mirrors (some report 625,783). Paper uses 80/20 split, standard scaling, SelectKBest ANOVA k=70, pseudo-sequence shape (70,1), CNN+GRU+cross-modal attention, ADASYN or ProWRAS applied training-only, Nadam learning rate .001, batch 512, at most 25 epochs, early stopping, validation holdout. Reported binary accuracy 1.0000, category accuracy 0.9995, sub-category accuracy 0.8228/0.8225 (ADASYN/ProWRAS).

**Do not claim reproduced:** paper source code is "available upon reasonable request", no exact complete implementation provided publicly. The notebook below implements a *paper-inspired* architecture and compares results, whereas `scripts/train_model.py` trains a deployable Random Forest baseline (not the paper model). Paper's sampling ProWRAS requires a reliable compatible implementation not shipped here. Label encoding, duplicated flows, feature types, version-dependent behavior, and differing row counts can cause score discrepancies.

**No dataset or evaluated results supplied in this archive** because network Kaggle download is blocked in this build environment. The downloader requires network + Kaggle access and must run on your machine. If the provided trainable baseline succeeds, it saves actual metrics in `docs/actual_metrics.json` and exports a trusted, fitted pipeline bundle.
