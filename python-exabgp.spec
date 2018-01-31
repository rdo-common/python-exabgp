%if 0%{?fedora}
%global with_python3 1
%endif
%global srcname exabgp

Name:           python-exabgp
Version:        4.0.5
Release:        4%{?dist}
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
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Requires:       python2-six
# XXX: only required for healthcheck.py on python2
# healthcheck.py is in service package, but it simplifies packaging to put it here
# According code, it tries to load ipaddress then ipaddr, since ipaddr is unmaintained
# Let's stick to ipaddress which is backport from python3 stdlib
Requires:       python2-ipaddress
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
The BGP swiss army knife of networking

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        The BGP swiss army knife of networking
Group:          Applications/Internet
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3-six
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
The BGP swiss army knife of networking
%endif

%package -n exabgp
Summary:        The BGP swiss army knife of networking
Group:          Applications/Internet
BuildRequires:  systemd-units
Requires:       systemd
# XXX: when python3 variant becomes default, change to python3 subpackage
Requires:                   python2-%{srcname} = %{version}-%{release}

%description -n exabgp
The BGP swiss army knife of networking (exabgp systemd unit)

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
# Now, we'll ensure that our python2 binaries does not get overwritten
# XXX: setup.py installs binaries in /usr/bin but systemd unit expects it to be in /usr/sbin
mkdir -p %{buildroot}%{_sbindir}
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{srcname} %{buildroot}%{_sbindir}/%{srcname}-%{python3_version}
ln -s ./%{srcname}-%{python3_version} %{buildroot}%{_sbindir}/%{srcname}-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/%{srcname} %{buildroot}%{_sbindir}/%{srcname}-%{python2_version}
ln -s ./%{srcname}-%{python2_version} %{buildroot}%{_sbindir}/%{srcname}-2
# Symbolic link to default exabgp binary variant (python2)
ln -s ./%{srcname}-2 %{buildroot}%{_sbindir}/%{srcname}

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif

# Install health check
install -p -D -m 0755 bin/healthcheck %{buildroot}%{_sbindir}
mv %{buildroot}%{_sbindir}/healthcheck %{buildroot}/%{_sbindir}/%{srcname}-healthcheck

# Install exabgpcli
install -p -D -m 0755 bin/exabgpcli %{buildroot}%{_bindir}

# Configure required directories for the exabgp service
mkdir -p %{buildroot}/%{_sysconfdir}/exabgp
mkdir -p %{buildroot}/%{_libdir}/exabgp
# Install exabgp systemd unit
mkdir -p %{buildroot}/%{_unitdir}
install -p -D -m 0644 etc/systemd/%{srcname}.service %{buildroot}/%{_unitdir}/%{srcname}.service

# Install man pages
mkdir -p %{buildroot}/%{_mandir}/man1
install doc/man/exabgp.1 %{buildroot}/%{_mandir}/man1
mkdir -p %{buildroot}/%{_mandir}/man5
install doc/man/exabgp.conf.5 %{buildroot}/%{_mandir}/man5

%post -n exabgp
%systemd_post %{srcname}.service

%preun -n exabgp
%systemd_preun %{srcname}.service

%postun -n exabgp
%systemd_postun_with_restart %{srcname}.service

%files -n python2-%{srcname}
%doc CHANGELOG README.md
%{python2_sitelib}/*
# XXX: when python3 variant becomes default, move next line to python3 subpackage
%{_sbindir}/%{srcname}
%{_sbindir}/%{srcname}-2*
%license COPYRIGHT

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{python3_sitelib}/*
%{_sbindir}/%{srcname}-3*
%doc CHANGELOG README.md
%license COPYRIGHT
%endif

# Let's split out exabgp service here
%files -n exabgp
%attr(755, root, root) %{_sbindir}/%{srcname}-healthcheck
%attr(755, root, root) %{_bindir}/exabgpcli
%{_unitdir}/%{srcname}.service
%dir %{_libdir}/%{srcname}
%dir %{_datadir}/%{srcname}
%dir %{_datadir}/%{srcname}/processes
%dir %{_sysconfdir}/%{srcname}
%attr(744, root, root) %{_datadir}/%{srcname}/processes/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Jan 31 2018 Luke Hinds <lhinds@redhat.com> - 4.0.5
- 4.0.5 release

* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.0.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 10 2017 Luke Hinds <lhinds@redhat.com> - 4.0.1-2
- Fixed dependency issues
* Fri Jul 07 2017 Luke Hinds <lhinds@redhat.com> - 4.0.1
- 4.0.1 release, and python 3 support
* Fri May 19 2017 Luke Hinds <lhinds@redhat.com> - 4.0.0
- Initial release
