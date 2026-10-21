.PHONY: help setup repro status clean

help:
	@echo "Cibles disponibles :"
	@echo "  make setup   Installer les dépendances du projet avec uv"
	@echo "  make repro   Exécuter ou mettre à jour la pipeline DVC"
	@echo "  make status  Vérifier l’état de la pipeline DVC"
	@echo "  make clean   Supprimer les données générées (conserve le CSV brut)"

setup:
	uv sync

repro:
	uv run dvc repro

status:
	uv run dvc status

clean:
	rm -f data/processed_data/X_train.csv \
	      data/processed_data/X_test.csv \
	      data/processed_data/y_train.csv \
	      data/processed_data/y_test.csv \
	      data/processed_data/X_train_scaled.csv \
	      data/processed_data/X_test_scaled.csv \
	      data/predictions.csv \
	      models/best_params.pkl \
	      models/model.pkl \
	      metrics/scores.json
