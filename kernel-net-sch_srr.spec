#
# TODO:
# - pl desc
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_without	up		# don't build UP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	SSR packets scheduler (Simple Round Robin)
Summary(pl.UTF-8):	Zarządca pakietów SRR (prosty algorytm karuzelowy)
Name:		kernel%{_alt_kernel}-net-sch_srr
Version:	0.4
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://mordor.strace.net/sched-srr/sch_srr.v%{version}.tgz
# Source0-md5:	943ed9d1a237336085331d43050d955c
URL:		http://mordor.strace.net/sched-srr/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains SRR packets scheduler (Simple Round Robin).

Simple Round Robin packets schedules - this is the schedules of
packets for the linux operating system with kernels 2.4 or 2.6. Its
purpose is the simply round robin distribution of the resources of the
allocated bandwidth between its users. It works as follows: the
internal queue of scheduler is divided into the given number of
virtual queues (slots). Each slot, in turn, has hard limited number of
packets located in it. Internal classifier distributes the entering in
scheduler packets along the slots, being based either on source ip
address or on destination ip address. With the selection of packet
from the scheduler, the slots will be processed cyclically, which will
ensure more or less uniform distribution.

%description -l pl.UTF-8
Prosty algorytm karuzelowy przeznaczony dla linuksa z jądrem 2.4 lub
2.6. Jego zadaniem jest zarządzanie dostępnym pasmem pomiędzy
wszystkich użytkowników. Prosty algorytm karuzelowy (SRR) działa w
następujący sposób: kolejka wewnętrzna zarządcy jest dzielona na
wirtualne kolejki (sloty). Każdy slot w każdym cyklu posiada stałą
liczbę pakietów, którymi zarządza. Wewnętrzny klasyfikator dzieli
wchodzące pakiety pomiędzy sloty używając do tego celu adresu
źródłowego lub docelowego. Sloty przetwarzane są karuzelowo
(cyklicznie) co zapewnia mniej lub bardziej sprawiedliwą dystrybucję
pakietów.

%package -n kernel%{_alt_kernel}-smp-net-sch_srr
Summary:	SSR packets scheduler (Simple Round Robin)
Summary(pl.UTF-8):	Zarządca pakietów SRR (prosty algorytm karuzelowy)
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-net-sch_srr
This package contains the Linux SMP driver for the SRR packets
scheduler.

%description -n kernel%{_alt_kernel}-smp-net-sch_srr -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa SMP do zarządcy pakietów SRR.

%prep
%setup -q -n sch_srr.v%{version}

cat > Makefile <<'EOF'
obj-m := sch_srr.o
CFLAGS += -DKERNEL26
EOF

%build
%build_kernel_modules  -m sch_srr

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m sch_srr -d kernel/net/sched

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-sch_srr
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-net-sch_srr
%depmod %{_kernel_ver}smp

%if %{with up}
%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/net/sched/sch_srr*.ko*
%endif

%if %{with smp}
%files -n kernel%{_alt_kernel}-smp-net-sch_srr
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/net/sched/sch_srr*.ko*
%endif
