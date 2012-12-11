%define modname wbxml
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A93_%{modname}.ini

Summary:	WBXML to XML conversion for PHP
Name:		php-%{modname}
Version:	1.0.3
Release:	%mkrel 17
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/wbxml
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Source1:	%{modname}.ini
Patch0:		wbxml-1.0.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch1:		wbxml-1.0.3-expat_fix.diff
BuildRequires:	php-devel >= 3:5.2.1
BuildRequires:	dos2unix
BuildRequires:	expat-devel
BuildRequires:	wbxml-devel
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
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix

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



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-17mdv2012.0
+ Revision: 795527
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-16
+ Revision: 761342
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-15
+ Revision: 696487
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-14
+ Revision: 695488
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-13
+ Revision: 646701
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-12mdv2011.0
+ Revision: 629898
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-11mdv2011.0
+ Revision: 628207
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-10mdv2011.0
+ Revision: 600547
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-9mdv2011.0
+ Revision: 588884
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-8mdv2010.1
+ Revision: 514713
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-7mdv2010.1
+ Revision: 485499
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-6mdv2010.1
+ Revision: 468270
- rebuilt against php-5.3.1

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-5mdv2010.0
+ Revision: 453361
- fix build
- fix deps
- rebuild
- rebuilt for php-5.3.0RC2

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Wed Mar 11 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1mdv2009.1
+ Revision: 353956
- 1.0.3

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2009.1
+ Revision: 346703
- rebuilt for php-5.2.9

* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2009.1
+ Revision: 344739
- fix deps
- import php-wbxml


* Wed Feb 25 2009 Oden Eriksson <oeriksson@mandriva.org> 1.0.2-1mdv2009.1
- initial Mandriva package
