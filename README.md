# README - Hive Metastore + Spark + Iceberg + MinIO + DBT

## Objectif

Mettre en place une plateforme analytique distribuée permettant :

* La lecture de tables Iceberg stockées dans un bucket MinIO
* La transformation des données via DBT et Apache Spark
* L'écriture des résultats dans un second bucket Iceberg (ciblé)

## Stack Technique

| Composant      | Version                  | Rôle                                   |
| -------------- | ------------------------ | -------------------------------------- |
| Apache Spark   | 3.5.3                    | Moteur de traitement distribue         |
| Apache Iceberg | 1.7.2                    | Format de table ACID                   |
| Hive Metastore | 3.1.3                    | Gestionnaire de métadonnées centralisé |
| PostgreSQL     | 15 (alpine)              | Backend du Metastore Hive              |
| MinIO          | latest                   | Stockage S3-compatible                 |
| DBT            | Core 1.7.7 + Spark 1.7.1 | Orchestration SQL                      |

## Arborescence du Projet

```
HIVE-METASTRORE-ICEBERG/
├── docker/                    # Dockerfiles personnalisés
├── dbt/                       # Modèles et configuration DBT
├── spark/                     # Scripts Spark (Thrift server)
│   └── start-thriftserver.sh
├── scripts/                   # Entrypoint Hive et téléchargements
├── config/                    # Configuration Hive
├── docker-compose.yml         # Déploiement multi-service
├── .gitignore
├── Makefile
└── .env                       # Configuration non versionnée
```

## Services Docker

### spark-master

* Conteneur Spark avec Thrift Server pour exécution SQL via DBT

### hive-metastore

* Serveur Hive connecté à PostgreSQL pour stocker les métadonnées

### hms-postgres

* Base de données PostgreSQL pour Hive Metastore

### minio

* Interface S3-compatible exposant deux buckets : source et target

### dbt

* Conteneur dédié à l'orchestration DBT pour exécuter des transformations SQL

## Utilisation

### 1. Télécharger les dépendances (JARs)

```bash
bash scripts/manual-download-dependencies.sh
```

### 2. Lancer les services

```bash
docker compose up -d --build
```

### 3. Tester la connexion DBT

```bash
docker compose run --rm dbt debug
```

### 4. Exécuter une transformation

```bash
docker compose run --rm dbt run
```

## Multi-catalogue Iceberg

Deux catalogues sont définis dans Spark Thrift Server :

| Nom    | URI                          | Warehouse                      |
| ------ | ---------------------------- | ------------------------------ |
| source | thrift://hive-metastore:9083 | s3a://iceberg-source/warehouse |
| target | thrift://hive-metastore:9083 | s3a://iceberg-target/warehouse |

> Le catalogue `spark_catalog` pointe vers le bucket `iceberg-target` et est utilisé par défaut dans DBT.

## Exemple de transformation DBT

```sql
-- dbt/models/my_table.sql
SELECT * FROM source.default.my_raw_table
```

Ce modèle créera une table Iceberg dans :
`s3a://iceberg-target/warehouse/default/my_table`

## Fichiers ignorés

Le `.gitignore` exclut :

* `.env`, credentials sensibles
* `*.jar`, dépendances téléchargeables
* `dbt/target`, `dbt/logs` et fichiers temporaires

## Améliorations futures

* Ajout de CI/CD pour DBT
* Intégration Dremio / Hue / Superset
* Déploiement sur Kubernetes (dossier présent)

## Licence

Projet open source sous licence MIT.
