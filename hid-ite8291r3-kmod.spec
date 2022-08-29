%global commit 48e04cb96517f8574225ebabb286775feb942ef5
%global shortcommit %(c=%{commit}; echo ${c:0:7})


%define buildforkernels akmod
%global debug_package %{nil}


# name should have a -kmod suffix
Name:           hid-ite8291r3-kmod
Version:        0.0
Release:        1%{?dist}.1
Summary:        Kernel module for the ITE 8291 (rev 0.03) RGB keyboard backlight controller
License:        GPLv2
URL:            https://github.com/pobrn/hid-ite8291r3
Source0:        %{URL}/archive/%{commit}/hid-ite8291r3-%{shortcommit}.tar.gz
Source1:        99-ite8291r3.rules


Patch0: Makefile.patch


# Verify that the package build for all architectures.
# In most time you should remove the Exclusive/ExcludeArch directives
# and fix the code (if needed).
ExclusiveArch:  x86_64


%global AkmodsBuildRequires %{_bindir}/kmodtool xz time elfutils-libelf-devel gcc bc
BuildRequires:  %{AkmodsBuildRequires}


# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo fedora --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }


%description
%{summary}.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}


# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo fedora --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null


%setup -q -c


# apply patches and do other stuff here
pushd hid-ite8291r3-%{commit}
%patch0 -p1
popd


for kernel_version in %{?kernel_versions} ; do
    cp -a hid-ite8291r3-%{commit} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    pushd  _kmod_build_${kernel_version%%___*}
    make %{?_smp_mflags} KDIR=${kernel_version##*___}
    popd
done


%install
%{__install} -d %{buildroot}%{_sysconfdir}/udev/rules.d/
%{__install} %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/

# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

for kernel_version in %{?kernel_versions}; do
    install -d %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done


%{?akmod_install}


%files
%license hid-ite8291r3-%{commit}/LICENSE
%doc hid-ite8291r3-%{commit}/README.md
%{_sysconfdir}/udev/rules.d/99-ite8291r3.rules


%changelog

