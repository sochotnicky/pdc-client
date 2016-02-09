%if 0%{?fedora}
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

# upstream has no support now, some dependencies are missing
%global with_python3 0

Name:           pdc-client
Version:        0.2.0.2
Release:        2%{?dist}
Summary:        Client library and console client for Product Definition Center
License:        MIT
URL:            https://github.com/product-definition-center/pdc-client
BuildArch:      noarch

Source0:        https://pypi.python.org/packages/source/p/pdc-client/pdc-client-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose
BuildRequires:  pytest
BuildRequires:  python-requests
BuildRequires:  python-requests-kerberos
BuildRequires:  python-mock
BuildRequires:  python2-beanbag

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
BuildRequires:  python3-requests-kerberos
BuildRequires:  python3-mock
BuildRequires:  python3-beanbag
%endif # if with_python3


# default to v2 since py3 doesnt' exist really
Requires:  python2-pdc-client = %{version}-%{release}

%description
This client package contains two separate Product Definition Center clients and
API module. Both clients contain extensive built-in help. Just run the
executable with -h or --help argument.

1. pdc_client

This is a very simple client. Essentially this is just a little more convenient
than using curl manually. Each invocation of this client obtains a token and
then performs a single request.

This client is not meant for direct usage, but just as a helper for integrating
with PDC from languages where it might be easier than performing the network
requests manually.

2. pdc

This is much more user friendly user interface. A single invocation can perform
multiple requests depending on what subcommand you used.

The pdc client supports Bash completion if argcomplete Python package is
installed.

3. Python API (pdc_client)

When writing a client code interfacing with PDC server, you might find
pdc_client module handy. It provides access to the configuration defined above
and automates obtaining authorization token.

%package -n python2-pdc-client
Summary:    Python 2 client library for Product Definition Center
%{?python_provide:%python_provide python2-pdc-client}
Requires:  python2-beanbag
Requires:  python-requests-kerberos

%description -n python2-pdc-client
This is a python module for interacting with Product Definition Center
programatically. It can handle common authentication and configuration of PDC
server connections

%package -n python3-pdc-client
Summary:    Python 3 client library for Product Definition Center

%{?python_provide:%python_provide python3-pdc-client}
Requires:  python3-beanbag
Requires:  python3-requests-kerberos

%description -n python3-pdc-client
This is a python module for interacting with Product Definition Center
programatically. It can handle common authentication and configuration of PDC
server connections

%prep
%setup -q -n pdc-client-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif # with_python3

%check
%{__python2} setup.py nosetests || exit 1

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py nosetests || exit 1
popd
%endif # with_python3

%install
%py2_install
%if 0%{?with_python3}
py3_install
%endif # with_python3

mkdir -p %{buildroot}/%{_mandir}/man1
cp docs/pdc_client.1 %{buildroot}/%{_mandir}/man1/

mkdir -p %{buildroot}/%{_sysconfdir}/bash_completion.d/
cp pdc.bash %{buildroot}/%{_sysconfdir}/bash_completion.d/

mkdir -p %{buildroot}/%{_sysconfdir}/pdc
cat > %{buildroot}/%{_sysconfdir}/pdc/client_config.json << EOF
{
    "dev": {
        "host": "https://pdc.fedoraproject.org/rest_api/v1/",
        "develop": false,
        "insecure": false
    }
}
EOF


%files
%doc README.markdown
%{_mandir}/man1/pdc_client.1*
%{_sysconfdir}/bash_completion.d
%dir %{_sysconfdir}/pdc
%config(noreplace) %{_sysconfdir}/pdc/client_config.json
%{_bindir}/pdc
%{_bindir}/pdc_client

%files -n python2-pdc-client
%doc README.markdown
%license LICENSE
%{python_sitelib}/pdc_client*

%if 0%{?with_python3}
%files -n python3-pdc-client
%doc README.markdown
%license LICENSE
%{python3_sitelib}/pdc_client*
%endif # with_python3


%changelog
* Mon Feb 08 2016 Ralph Bean <rbean@redhat.com> - 0.2.0.2-2
- Point default configuration at Fedora's prod instance.

* Fri Jan 22 2016 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.2.0.2-1
- Rebase to latest upstream

* Mon Jan 11 2016 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.1.9-1
- Initial version

* Fri Dec 04 2015 Xiangyang Chu <xchu@redhat.com> 0.2.0-1
- Add python 2.6 check. (xchu@redhat.com)
- Fix spec URL (rbean@redhat.com)
- Allow PDCClient to be configured with arguments. (rbean@redhat.com)
- Imporvements on new `pdc` client.
* Fri Sep 11 2015 Xiangyang Chu <xychu2008@gmail.com> 0.1.0-1
- new package built with tito
