ENGINE := /usr/bin/podman
REGISTRYNAME := gitea.fabiv.pw/fborries/utilities
CONTAINERNAME := $(REGISTRYNAME)/k8s-mgmt
TARGETLIST := base cilium cilium-clusterctl cilium-talosctl istio istio-clusterctl istio-talosctl clusterctl talosctl
CONTAINERLIST := $(foreach target,$(TARGETLIST),$(CONTAINERNAME):$(target))

.PHONY: all
all: $(TARGETLIST)

.PHONY: clean
clean:
	$(ENGINE) rmi -fi $(CONTAINERLIST)

.PHONY: login
login:
	$(ENGINE) login $(REGISTRYNAME)

.PHONY: push
push: login
	$(foreach target,$(CONTAINERLIST),$(shell podman image exists $(target) && podman push $(target)))

.PHONY: base
base:
	$(ENGINE) build . -t $(CONTAINERNAME):$@ --target $@

.PHONY: clusterctl cilium istio
clusterctl cilium istio: base
	$(ENGINE) build . -t $(CONTAINERNAME):$@ --target $@

.PHONY: talosctl
talosctl: clusterctl
	$(ENGINE) build . -t $(CONTAINERNAME):$@ --target $@

.PHONY: cilium-clusterctl
cilium-clusterctl: cilium
	$(ENGINE) build . -t $(CONTAINERNAME):$@ --build-arg SERVICEMESH="cilium" --target clusterctl

.PHONY: cilium-talosctl
cilium-talosctl:
	$(ENGINE) build . -t $(CONTAINERNAME):$@ --build-arg SERVICEMESH="cilium" --target talosctl

.PHONY: istio-clusterctl
istio-clusterctl: istio
	$(ENGINE) build . -t $(CONTAINERNAME):$@ --build-arg SERVICEMESH="istio" --target clusterctl

.PHONY: istio-talosctl
istio-talosctl: istio
	$(ENGINE) build . -t $(CONTAINERNAME):$@ --build-arg SERVICEMESH="istio" --target talosctl
