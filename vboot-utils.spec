Name:		vboot-utils
Version:	20130222gite6cf2c2
Release:	2
Summary:	Verified Boot Utility from Chromium OS
ExclusiveArch:	%{arm} %{ix86} x86_64

Group:		System/Base
License:	BSD
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  git clone https://git.chromium.org/git/chromiumos/platform/vboot_reference.git
#  cd vboot_reference/
#  git archive --format=tar --prefix=vboot-utils-20130222gite6cf2c2/ e6cf2c2 | xz > vboot-utils-20130222gite6c.tar.xz
URL:		http://gitrw.chromium.org/gitweb/?p=chromiumos/platform/vboot_reference.git
Source0:	%{name}-%{version}.tar.xz
## Patch0 disabled static building.
Patch0:		vboot-utils-00-disable-static-linking.patch
## Patch1 fixes printf formating issues that break  the build.
## http://code.google.com/p/chromium-os/issues/detail?id=37804
Patch1:		vboot-utils-01-bmpblk_utility-fix-printf.patch
#make sure get the rpmbuild flags passed in
Patch2:		vboot-utils-cflags.patch
# some fixes for picker compile
Patch3:		vboot-utils-strncat.patch
Patch4:		vboot-utils-unused.patch
Patch5:		vboot-utils-pthread.patch


BuildRequires:	openssl-devel
BuildRequires:	trousers-devel
BuildRequires:	yaml-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(uuid)

# for the test scripts
BuildRequires:	python

%description
Verified boot is a collection of utilities helpful for chromebook computer.
Pack and sign the kernel, manage gpt partitions.


%prep
%setup -q
%patch0 -p0 -b .nostatic
%patch1 -p0 -b .fixprintf
%patch2 -p1 -b .cflags
%patch3 -p1 -b .strncat
%patch4 -p1 -b .unused
%patch5 -p1 -b .pthread

sed -e 's:-Werror ::g' -e 's:-nostdinc ::g' -i Makefile

%build
%ifarch %{arm}
%define ARCH arm
%endif

%ifarch x86_64
%define ARCH x86_64
%endif

%ifarch %{ix86}
%define ARCH i386
%endif

make V=1 ARCH=%{ARCH} COMMON_FLAGS="$RPM_OPT_FLAGS"

%install
make install V=1 DESTDIR=%{buildroot}%{_bindir} ARCH=%{ARCH} COMMON_FLAGS="$RPM_OPT_FLAGS"

## Tests are enabled but ignored (will not break the build).
## This is because tests fail in a chroot (mock) but work otherwise.
%check
make runtests || true


%files
%{_bindir}/*
%doc LICENSE README
