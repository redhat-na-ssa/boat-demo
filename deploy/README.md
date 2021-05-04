Prereqs
=======

- Cluster w/storage
- Registry running
- ODH operator installed on cluster


Deployment Steps
================

1. Create namespace
```
oc apply -f 01-namespace.yaml
```

2. Create ODH instance
```
oc apply -f 02-odh.yaml
```

3. Build Jupyter Lab working environment
```
oc apply -f 03-notebook-image.yaml
```

4. Create OpenGL enabled Python S2I builder.
```
oc apply -f 04-s2i-builder.yaml
```

5. Create boat-detect microservice.
```
oc apply -f 05-boat-detect-app.yaml
```

6. Create boat-identify microservice.
```
oc apply -f 06-boat-identify-app.yaml
```

7. Create boat-group microservice.
```
oc apply -f 07-boat-group-app.yaml
```

8. Create JupyterHub user profiles.
```
sed -i 's/USERNAME/example_user_1/g' 08-jupyterhub-user-profiles.yaml
oc apply -f 08-jupyterhub-user-profiles.yaml
git checkout 08-jupyterhub-user-profiles.yaml
```

