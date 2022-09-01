%global commit 48e04cb96517f8574225ebabb286775feb942ef5
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global debug_package %{nil}

#define buildforkernels newest
#define buildforkernels current
%define buildforkernels akmod



Name:           hid-ite8291r3-kmod
Version:        0.0
Release:        4%{?dist}
Summary:        Kernel module for the ITE 8291 (rev 0.03) RGB keyboard backlight controller
License:        GPLv2
URL:            https://github.com/pobrn/hid-ite8291r3
Source0:        %{URL}/archive/%{commit}/hid-ite8291r3-%{shortcommit}.tar.gz
Patch0:         Makefile.patch

ExclusiveArch:  x86_64
%global AkmodsBuildRequires %{_bindir}/kmodtool xz time elfutils-libelf-devel gcc bc
BuildRequires:  %{AkmodsBuildRequires}

%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }



%description
%{summary}.



%prep
%{?kmodtool_check}

kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c

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
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

for kernel_version in %{?kernel_versions}; do
    install -d %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
    install _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done
%{?akmod_install}



%changelog
* Thu Sep 01 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.0-4
- Used both version and release in requires and provides for common package

* Wed Aug 31 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.0-3
- Changed build for kernels to be akmod
- removed unnecessry build dependencies

* Tue Aug 30 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.0-2
- Fixed version and release numbers

* Mon Aug 29 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.1-1
- First version of kernel module - hid-ite8291r3-kmod

