%{?_javapackages_macros:%_javapackages_macros}
%global base_name  jci
%global short_name commons-%{base_name}
%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}

Name:          apache-commons-jci
Version:       1.0
Release:       10.0%{?dist}
Summary:       Commons Java Compiler Interface
License:       ASL 2.0
URL:           http://commons.apache.org/jci/
Source0:       ftp://ftp.gbnet.net/pub/apache/dist/commons/%{base_name}/source/%{short_name}-%{namedversion}-src.tar.gz
# force ecj 4.x use
Source1:       %{name}-%{namedversion}-depmap
# fix parent relative path
# fix groovy gId and aId
# add org.codehaus.janino commons-compiler
# remove org.codehaus.mojo findbugs-maven-plugin 1.0.0
Patch0:        %{name}-%{namedversion}-fixbuild.patch
# asm 3 test build
Patch1:        %{name}-%{namedversion}-ExtendedDump.patch
Patch2:        %{name}-%{namedversion}-SimpleDump.patch
# fix parent relative path
# remove jetty-maven-plugin
# use tomcat 7.x apis
Patch3:        %{name}-%{namedversion}-examples-pom.patch

Patch4:        %{name}-%{namedversion}-janino26.patch

Patch5:        %{name}-%{namedversion}-ecj4.patch

BuildRequires: java-devel

BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-plugin-cobertura
BuildRequires: maven-site-plugin
BuildRequires: maven-surefire-provider-junit4

BuildRequires: apache-commons-logging
BuildRequires: apache-commons-io
BuildRequires: ecj >= 3.4.2-13
BuildRequires: groovy
BuildRequires: janino
BuildRequires: rhino

# test deps
BuildRequires: apache-commons-lang
BuildRequires: junit
BuildRequires: objectweb-asm
%if 0%{?fedora}
%else
BuildRequires: mvn(org.eclipse.jdt:core)
%endif

Requires:      %{name}-core = %{version}-%{release}
BuildArch:     noarch

#* javac Commons JCI compiler implementation for the javac compiler (up to JDK 1.5).
#* jsr199 Commons JCI compiler implementation for JDK 1.6 and up.

%description
JCI is a java compiler interface featuring a compiling class loader.
The current implementation supports compilation via the following
compilers:

* eclipse
* groovy
* janino
* rhino

%package core
Summary:       Commons Java Compiler Interface - core

%description core
Commons JCI core interfaces and implementations.

%package fam
Summary:       Commons Java Compiler Interface - FAM

%description fam
Commons JCI FileAlterationMonitor (FAM) to
monitor local file systems and get notified
about changes.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

# compilers

%package eclipse
Summary:       Commons Java Compiler Interface - eclipse

%description eclipse
Commons JCI compiler implementation for the eclipse compiler.

%package groovy
Summary:       Commons Java Compiler Interface - groovy

%description groovy
Commons JCI compiler implementation for the groovy compiler.

%package janino
Summary:       Commons Java Compiler Interface - janino

%description janino
Commons JCI compiler implementation for the janino compiler.

%package rhino
Summary:       Commons Java Compiler Interface - rhino

%description rhino
Commons JCI compiler implementation for rhino JavaScript.

%prep
%setup -q -n %{short_name}-%{namedversion}-src
find . -name "*.class" -delete
find . -name "*.jar" -delete

%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p0

# require old version of jdependency
%pom_disable_module compilers/javac
%pom_disable_module examples

sed -i "s|<maven.compile.source>1.4<|<maven.compile.source>1.5<|" pom.xml
sed -i "s|<maven.compile.target>1.4<|<maven.compile.target>1.5<|" pom.xml

# Fix installation directory      

%mvn_file :%{short_name}-core    %{short_name}/%{short_name}-core
%mvn_file :%{short_name}-fam     %{short_name}/%{short_name}-fam
%mvn_file :%{short_name}-eclipse %{short_name}/%{short_name}-eclipse
%mvn_file :%{short_name}-groovy  %{short_name}/%{short_name}-groovy
%mvn_file :%{short_name}-janino  %{short_name}/%{short_name}-janino
%mvn_file :%{short_name}-rhino   %{short_name}/%{short_name}-rhino

%build

# random tests failures
%mvn_build -s -- -Dmaven.test.failure.ignore=true -Dmaven.local.depmap.file="%{SOURCE1}"

%install
%mvn_install

%files
%dir %{_javadir}/%{short_name}
%{_mavendepmapfragdir}/apache-commons-jci-commons-jci.xml
%if 0%{?fedora}
%{_mavenpomdir}/JPP.apache-commons-jci-org.apache.commons@commons-jci.pom
%else
%{_mavenpomdir}/JPP.apache-commons-jci-commons-jci.pom
%endif
%doc LICENSE.txt NOTICE.txt README.txt TODO.txt

%files core -f .mfiles-%{short_name}-core

%files fam -f .mfiles-%{short_name}-fam

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%files eclipse -f .mfiles-%{short_name}-eclipse

%files groovy -f .mfiles-%{short_name}-groovy

%files janino -f .mfiles-%{short_name}-janino

%files rhino -f .mfiles-%{short_name}-rhino

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 gil cattaneo <puntogil@libero.it> 1.0-9
- switch to XMvn, minor changes to adapt to current guideline

* Wed Jun 12 2013 Orion Poplawski <orion@cora.nwra.com> - 1.0-8
- Make main package own jar directory

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Dec 12 2012 gil cattaneo <puntogil@libero.it> 1.0-5
- fix build for new ecj

* Thu Jul 19 2012 gil cattaneo <puntogil@libero.it> 1.0-4
- Add depmap file, force ecj use

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 gil cattaneo <puntogil@libero.it> 1.0-2
- javadocs are installed in %%{_javadocdir}/%%{name}
- correct spelling errors
- fix requires

* Fri Apr 06 2012 gil cattaneo <puntogil@libero.it> 1.0-1
- initial rpm
