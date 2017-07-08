%if 0%{?fedora}
%global with_python3 1
%endif
%global srcname exabgp

Name:           python-exabgp
Version:        4.0.1
Release:        1%{?dist}
Summary:        The BGP swiss army knife of networking (Library)

License:        BSD
URL:            https://github.com/Exa-Networks/
Source0:        https://github.com/Exa-Networks/%{srcname}/archive/%{version}.tar.gz

BuildArch:      noarch

%description
ExaBGP python module

%package -n python2-%{srcname}
Summary:        The BGP swiss army knife of networking
Group:          Applications/Internet
BuildRequires:  systemd-units
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:       python-ipaddr
Requires:       python2-six
Requires:       python-exabgp
Requires:       systemd
Requires: %{name} = %{version}-%{release}

%description -n python2-%{srcname}
The BGP swiss army knife of networking

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        The BGP swiss army knife of networking
Group:          Applications/Internet
BuildRequires:  systemd-units
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python-ipaddr
Requires:       python3-six
Requires:       python-exabgp
Requires:       systemd
Requires: %{name} = %{version}-%{release}
%endif

%description -n python3-%{srcname}
The BGP swiss army knife of networking

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

install bin/healthcheck %{buildroot}%{_bindir}
mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
mv %{buildroot}%{_sbindir}/healthcheck %{buildroot}/%{_sbindir}/exabgp-healthcheck

mkdir -p %{buildroot}/%{_sysconfdir}/exabgp
mkdir -p %{buildroot}/%{_libdir}/exabgp

mkdir -p %{buildroot}/%{_unitdir}
install -p -D -m 0644 etc/systemd/exabgp.service %{buildroot}/%{_unitdir}/exabgp.service

mkdir -p %{buildroot}/%{_mandir}/man1
install doc/man/exabgp.1 %{buildroot}/%{_mandir}/man1

mkdir -p %{buildroot}/%{_mandir}/man5
install doc/man/exabgp.conf.5 %{buildroot}/%{_mandir}/man5

%post -n %{name}
%systemd_post exabgp.service

%preun -n %{name}
%systemd_preun exabgp.service

%postun -n %{name}
%systemd_postun_with_restart exabgp.service

%files -n python2-%{srcname}
%{python2_sitelib}/*
%defattr(-,root,root,-)
%doc CHANGELOG README.md
%license COPYRIGHT
%{_unitdir}/exabgp.service
%{_sbindir}/exabgp
%dir %{_libdir}/exabgp
%dir %{_datadir}/exabgp
%dir %{_datadir}/exabgp/processes
%dir %{_sysconfdir}/exabgp
%attr(744, root, root) %{_datadir}/exabgp/processes/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{python3_sitelib}/*
%defattr(-,root,root,-)
%doc CHANGELOG README.md
%license COPYRIGHT
%attr(755, root, root) %{_sbindir}/exabgp-healthcheck
%{_unitdir}/exabgp.service
%{_sbindir}/exabgp
%dir %{_libdir}/exabgp
%dir %{_datadir}/exabgp
%dir %{_datadir}/exabgp/processes
%dir %{_sysconfdir}/exabgp
%attr(744, root, root) %{_datadir}/exabgp/processes/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%endif

%changelog
* Fri Jul 07 2017 Luke Hinds <lhinds@redhat.com> - 4.0.1
- 4.0.1 release, and python 3 support
* Fri May 19 2017 Luke Hinds <lhinds@redhat.com> - 4.0.0
- Initial release
