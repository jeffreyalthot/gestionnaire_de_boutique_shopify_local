# Architecture

L’architecture sépare domaine, intégrations, workflows, workers, persistance, sécurité, IA et présentation. Les webhooks alimentent la table `events`, puis la file `tasks`. Les workers prennent un bail transactionnel avant exécution.
