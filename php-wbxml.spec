%define modname wbxml
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A93_%{modname}.ini

Summary:	WBXML to XML conversion for PHP
Name:		php-%{modname}
Version:	1.0.2
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/wbxml
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
Patch0:		wbxml-1.0.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch1:		wbxml-1.0.2-version_fix.diff
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	dos2unix
BuildRequires:	expat-devel
BuildRequires:	wbxml2-devel
BuildRequires:	popt-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This extension provides WBXML (Wireless Binary XML) conversion capabilities
using the libwbxml library, which can be found at
http://libwbxml.aymerick.com/

%prep

%setup -q -n %{modname}-%{version}
[ "../package.xml" != "/" ] && mv ../package.xml .

cp %{SOURCE1} %{inifile}

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

%patch0 -p0
%patch1 -p0

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix} \

%make
mv modules/*.so .

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc CREDITS README wbxml.php package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

