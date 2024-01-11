%global __python3 /usr/bin/python3.11
%global python3_pkgversion 3.11

# RHEL: Tests disabled due to missing dependencies
%bcond_with tests

Name:           python%{python3_pkgversion}-requests
Version:        2.28.1
Release:        1%{?dist}
Summary:        HTTP library, written in Python, for human beings

License:        ASL 2.0
URL:            https://pypi.io/project/requests
Source0:        https://github.com/requests/requests/archive/v%{version}/requests-v%{version}.tar.gz
# Explicitly use the system certificates in ca-certificates.
# https://bugzilla.redhat.com/show_bug.cgi?id=904614
Patch0:         requests-2.28.1-system-certs.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-charset-normalizer
BuildRequires:  python%{python3_pkgversion}-urllib3
BuildRequires:  python%{python3_pkgversion}-idna
# pygments is used for syntax highlighting in the docs - disabled due to missing deps
#BuildRequires:  python%%{python3_pkgversion}-pygments
BuildRequires:  python%{python3_pkgversion}-setuptools

%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-httpbin
BuildRequires:  python%{python3_pkgversion}-pytest-mock
BuildRequires:  python%{python3_pkgversion}-trustme
%endif

Requires:  python%{python3_pkgversion}-charset-normalizer
Requires:  python%{python3_pkgversion}-urllib3
Requires:  python%{python3_pkgversion}-idna 

%description
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.


%{?python_extras_subpkg:%python_extras_subpkg -n python%{python3_pkgversion}-requests -i %{python3_sitelib}/*.egg-info security socks}

%prep
%autosetup -p1 -n requests-%{version}

# env shebang in nonexecutable file
sed -i '/#!\/usr\/.*python/d' requests/certs.py

# Some doctests use the internet and fail to pass in Koji. Since doctests don't have names, I don't
# know a way to skip them. We also don't want to patch them out, because patching them out will
# change the docs. Thus, we set pytest not to run doctests at all.
sed -i 's/ --doctest-modules//' pyproject.toml


%build
%py3_build


%install
%py3_install


%if %{with tests}
%check
%pytest -v
%endif


%files -n python%{python3_pkgversion}-requests
%license LICENSE
%doc README.md HISTORY.md
%{python3_sitelib}/*.egg-info/
%{python3_sitelib}/requests/


%changelog
* Tue Nov 29 2022 Charalampos Stratakis <cstratak@redhat.com> - 2.28.1-1
- Initial package
- Fedora contributions by:
      Adam Williamson <awilliam@redhat.com>
      Arun SAG <sagarun@gmail.com>
      Charalampos Stratakis <cstratak@redhat.com>
      David Malcolm <dmalcolm@redhat.com>
      Dennis Gilmore <dennis@ausil.us>
      Igor Gnatenko <ignatenkobrain@fedoraproject.org>
      Iryna Shcherbina <shcherbina.iryna@gmail.com>
      Jeremy Cline <jeremy@jcline.org>
      Karolina Surma <ksurma@redhat.com>
      Kevin Fenzi <kevin@scrye.com>
      Lumir Balhar <lbalhar@redhat.com>
      Miro Hrončok <miro@hroncok.cz>
      Petr Viktorin <pviktori@redhat.com>
      Ralph Bean <rbean@redhat.com>
      Randy Barlow <randy@electronsweatshop.com>
      Rex Dieter <rdieter@math.unl.edu>
      Robert Kuska <rkuska@redhat.com>
      Slavek Kabrda <bkabrda@redhat.com>
      Stephen Gallagher <sgallagh@redhat.com>
      Tom Callaway <spot@fedoraproject.org>
      Toshio Kuratomi <toshio@fedoraproject.org>
      yatinkarel <ykarel@redhat.com>
