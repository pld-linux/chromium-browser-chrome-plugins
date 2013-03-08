# NOTE
# - this is obsolete, use google-chrome.spec to build plugin packages

%define		svnrev	186726
%define		state	stable_current
%define		rel		0.2
%define		google_name	google-chrome
Summary:	Plugins from Google Chrome for Chromium browser
Summary(pl.UTF-8):	Wtyczki z przeglądarki Google Chrome dla Chromium
Name:		chromium-browser-chrome-plugins
Version:	25.0.1364.160
Release:	%{svnrev}.%{rel}
License:	Multiple, see http://chrome.google.com/
Group:		Applications/Networking
Source0:	https://dl.google.com/linux/direct/%{google_name}-%{state}_i386.rpm
# Source0-md5:	82ef51944927db96c53f62e51b913a0a
Source1:	https://dl.google.com/linux/direct/%{google_name}-%{state}_x86_64.rpm
# Source1-md5:	9dbde8b12e03e0601afa2db69671599f
URL:		http://chrome.google.com/
BuildRequires:	rpm-utils
BuildRequires:	rpmbuild(macros) >= 1.453
Requires:	chromium-browser
Suggests:	%{name}-pdf
ExclusiveArch:	%{ix86} %{x8664}
%ifarch %{ix86}
Suggests:	%{name}-flash_player
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0
%define		no_install_post_strip	1

%define		ffmpeg_caps	libffmpegsumo.so
%define		jpeg_caps	libpng12.so.0(PNG12_0)
%define		flash_caps	libflashplayer.so libpepflashplayer.so
%define		chrome_caps	libpdf.so libppGoogleNaClPluginChrome.so

# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov		%{ffmpeg_caps} %{jpeg_caps} %{flash_caps} %{chrome_caps}
# do not require them either
%define		_noautoreq		%{_noautoprov}

%description
Plugins from Google Chrome for Chromium browser, which are not
included in Chromium due to license issues.


%description -l pl.UTF-8
Wtyczki z Google Chrome dla przeglądarki Chromium, które nie są
zawarte w Chromium ze względu na licencję.

%package pdf
Summary:	PDF plugin from Google Chrome
Summary(pl.UTF-8):	Wtyczka PDF z Google Chrome
Group:		X11/Applications/Graphics

%description pdf
PDF plugin from Google Chrome, which is not available in Chromium.

%description pdf -l pl.UTF-8
Wtyczka PDF z Google Chrome, która nie jest dostępna w Chromium.

%package flash_player
Summary:	Adobe Flash plugin from Google Chrome
Summary(pl.UTF-8):	Wtyczka Adobe Flash z Google Chrome
Group:		X11/Applications/Multimedia

%description flash_player
Adobe Flash plugin from Google Chrome, which is not available in
Chromium.

%description flash_player -l pl.UTF-8
Wtyczka Adobe Flash z Google Chrome, która nie jest dostępna w
Chromium.

Wtyczka Adobe Flash z Google Chrome, która nie jest dostępna w
Chromium.
%prep
%setup -qcT
%ifarch %{ix86}
SOURCE=%{S:0}
%endif
%ifarch %{x8664}
SOURCE=%{S:1}
%endif

V=$(rpm -qp --nodigest --nosignature --qf '%{V}' $SOURCE)
R=$(rpm -qp --nodigest --nosignature --qf '%{R}' $SOURCE)
if [ version:$V != version:%{version} -o svnrev:$R != svnrev:%{svnrev} ]; then
	exit 1
fi
rpm2cpio $SOURCE | cpio -i -d
mv opt/google/chrome .

chmod a+x chrome/lib*.so*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/chromium-browser/plugins

cp -a chrome/libpdf.so $RPM_BUILD_ROOT%{_libdir}/chromium-browser/plugins
%ifarch %{ix86}
cp -a chrome/libgcflashplayer.so $RPM_BUILD_ROOT%{_libdir}/chromium-browser/plugins
%endif
%ifarch %{x8664}
cp -a chrome/PepperFlash/{libpepflashplayer.so,manifest.json} $RPM_BUILD_ROOT%{_libdir}/chromium-browser/plugins
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%files pdf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/chromium-browser/plugins/libpdf.so

%files flash_player
%defattr(644,root,root,755)
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/chromium-browser/plugins/libgcflashplayer.so
%endif
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/chromium-browser/plugins/libpepflashplayer.so
%{_libdir}/chromium-browser/plugins/manifest.json
%endif
