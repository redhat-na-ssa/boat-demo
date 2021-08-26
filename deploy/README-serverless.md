# How to deploy the boat demo's services as OpenShift Serverless Functions

## Overview

As of today, OpenShift Serverless functions for this project are built, tested and deployed using a Fedora 34 bastion. 
This should improve as python serverless functions become generally available.

### Bastion host configuration

1) Install `podman` and `wget`

```
sudo dnf install -y podman wget
```

2) Create directories

```
mkdir -p .local/bin $HOME/.config/kn/plugins
```

3) Install the knative clients

```
wget https://github.com/knative/client/releases/download/v0.23.2/kn-linux-amd64
chmod u+x kn-linux-amd64
mv kn-linux-amd64 $HOME/.local/bin/kn
```

```
wget https://github.com/knative-sandbox/kn-plugin-func/releases/download/v0.16.0/func_linux_amd64.gz
gzip -d func_linux_amd64.gz
chmod u+x func_linux_amd64
mv func_linux_amd64 $HOME/.config/kn/plugins/kn-func
```

Verify
```
kn plugin list
```

Example output
```
- kn-func : /home/fedora/.config/kn/plugins/kn-func
```

Open a second terminal and start the podman API service.
```
podman system service --time=0 tcp:0.0.0.0:1234
```

### Build and deployment workflow

1) Install the `oc` binary from the [web console](https://console-openshift-console.apps.ocp.d1db.sandbox1682.opentlc.com/command-line-tools)
```
wget https://downloads-openshift-console.apps.ocp.d1db.sandbox1682.opentlc.com/amd64/linux/oc.tar -O - | tar x
mv oc $HOME/.local/bin
```

2) Get the hostname for the OpenShift registry

Login to an OpenShift cluster as an **admin** user then follow step 1 in the Red Hat docs to [expose the OpenShift registry](https://docs.openshift.com/container-platform/4.7/registry/securing-exposing-registry.html#registry-exposing-secure-registry-manually_securing-exposing-registry) and save the route.
```
HOST=$(oc get route default-route -n openshift-image-registry --template='{{ .spec.host }}')
echo $HOST
```

Example output
```
default-route-openshift-image-registry.apps.ocp.d1db.sandbox1682.opentlc.com
```

2) Login to the registry from podman.

Login to OpenShift as a **developer** user, change into the `boats-demo` project and login to the registry.

```
oc project boats-demo
podman login -u developer -p $(oc whoami -t) --tls-verify=false $HOST
```

Example output
```
Login Succeeded!
```

Configure the `podman` client.
```
export DOCKER_HOST=tcp://127.0.0.1:1234
```

Run a build
```
git clone https://github.com/redhat-naps-da/boat-demo.git
cd boats-demo/identify
kn func build --image=$HOST/boats-demo/identify
```

Example output
```
🙌 Function image built: default-route-openshift-image-registry.apps.ocp.d1db.sandbox1682.opentlc.com/boats-demo/identify
```

Deploy the service
```
kn func deploy
```

Example output
```
🕘 Deploying function to the cluster
Function deployed at URL: http://identify-serverless-boats-demo.apps.ocp.d1db.sandbox1682.opentlc.com
```

Configure and run the REST test client

Edit `01-client.py` and set the `IDENT_URL` variable with the service `URL` returned by the function deployment.

Example
```
IDENT_URL="http://identify-serverless-boats-demo.apps.ocp.d1db.sandbox1682.opentlc.com"
```

Run the test client
```
python 01-client.py
```

Example output
```
(datetime.datetime(2021, 4, 22, 3, 40, 31, 994728), None, {'objects': [{'box': [207.0, 509.0, 299.0, 532.0], 'confidence': 0.8941678404808044, 'class': 'boats', 'id': '0'}, {'box': [65.0, 326.0, 136.0, 403.0], 'confidence': 0.8731332421302795, 'class': 'boats', 'id': '1'}, {'box': [1066.0, 109.0, 1142.0, 171.0], 'confidence': 0.8629531264305115, 'class': 'boats', 'id': '2'}, {'box': [82.0, 602.0, 149.0, 671.0], 'confidence': 0.8608279228210449, 'class': 'boats', 'id': '3'}, {'box': [298.0, 438.0, 383.0, 461.0], 'confidence': 0.8419623374938965, 'class': 'boats', 'id': '4'}, {'box': [242.0, 0.0, 298.0, 19.0], 'confidence': 0.6364468932151794, 'class': 'boats', 'id': '5'}], 'tracking': {'next_id': 6, 'missing': {}}})
```

Repeat the same for the *group* service.

To build and deploy the *detect* service as a serverless function, buildpacks must be used
to custom build and runtime container images. A set of example Dockerfiles are provided in the
`serverless` directory. Refer to `serverless/buildpacks/stacks/python/build/Dockerfile` and `serverless//buildpacks/stacks/python/run/Dockerfile`. To build these images 
the [`pack` utility](https://github.com/buildpacks/pack) must be 
installed before a top level `make` command in the `serverless/buildpacks` directory is run. 

```
$ cd serverless/buildpacks
$ make
```

Once the build and run images are created, proceed as usual to build and deploy the *detect* serverless function using `kn func build` and `kn func deploy`.

#### Trouble Shooting

As of today, RHEL8.4 reports the following error when deploying probably due
to the version of `podman`. See https://issues.redhat.com/projects/SRVOCF/issues/SRVOCF-353?filter=allissues

```
kn func deploy

   Pushing function image to the registry
Error: failed to push the image: Error reading JSON: invalid character '{' after top-level value
```
