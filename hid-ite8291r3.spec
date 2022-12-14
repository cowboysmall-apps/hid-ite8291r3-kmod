%global commit 48e04cb96517f8574225ebabb286775feb942ef5
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global debug_package %{nil}



Name:           hid-ite8291r3
Version:        0.0
Release:        4%{?dist}
Summary:        Common package for the ITE 8291 (rev 0.03) RGB keyboard backlight controller
License:        GPLv2
URL:            https://github.com/pobrn/hid-ite8291r3
Source0:        %{URL}/archive/%{commit}/hid-ite8291r3-%{shortcommit}.tar.gz
Source1:        99-hid-ite8291r3.rules

ExclusiveArch:  x86_64
Requires: %{name}-kmod >= %{version}-%{release}
Provides: %{name}-kmod-common = %{version}-%{release}



%description
%{summary}.



%prep
%setup -q -c



%build
# nothing to build



%install
%{__install} -d %{buildroot}%{_sysconfdir}/udev/rules.d/
%{__install} %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/
%{?akmod_install}



%files
%license hid-ite8291r3-%{commit}/LICENSE
%doc hid-ite8291r3-%{commit}/README.md
%{_sysconfdir}/udev/rules.d/99-hid-ite8291r3.rules



%changelog
* Thu Sep 01 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.0-4
- Used both version and release in requires and provides

* Wed Aug 31 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.0-3
- Changed release to reflect kmod release

* Tue Aug 30 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.0-2
- Fixed version and release numbers

* Tue Aug 30 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.2-1
- Renamed udev rules file to avoid conflict with ite8291r3-ctl

* Mon Aug 29 2022 Jerry Kiely <jerry@cowboysmall.com> - 0.1-1
- First version of kernel module common files - hid-ite8291r3-kmod-common

