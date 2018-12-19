@ECHO OFF

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set BUILDDIR=build
set ALLSPHINXOPTS=-j %Number_Of_Processors% -d %BUILDDIR%/doctrees %SPHINXOPTS% manual
set I18NSPHINXOPTS=%SPHINXOPTS% manual
if NOT "%PAPER%" == "" (
	set ALLSPHINXOPTS=-D latex_paper_size=%PAPER% %ALLSPHINXOPTS%
	set I18NSPHINXOPTS=-D latex_paper_size=%PAPER% %I18NSPHINXOPTS%
)

REM Default to HTML
if "%1" == "" (
	echo.No command given, defaulting to html.
	echo.
	goto html
)

if "%1" == "help" (
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.
	echo.Documentation
	echo.=============
	echo.
	echo.Convenience targets provided for building docs
	echo.- html                 to make standalone HTML files ^(default^)
	echo.- singlehtml           to make a single large HTML file
	echo.- pdf                  to make a PDF using LaTeX warning: this currently has some problems,
	echo.                       though the PDF generates, there are various unresolved issues
	echo.- gettext              to make PO message catalogs
	echo.- epub                 to make an epub
	echo.- epub3                to make an epub3
  echo.- readme               to make a 'readme.html' file
	echo.- clean                to delete all old build files
	echo.
	echo.Translations
	echo.============
	echo.
	echo.- gettext              to make PO message catalogs
	echo.- update_po            to update PO message catalogs
	echo.- report_po_progress   to check the progress/fuzzy strings
	echo.
	echo.Checking
	echo.========
	echo.
	echo.- check_structure      to check the structure of all .rst files
	echo.- check_syntax         to check the syntax of all .rst files
	echo.- check_links          to check all external links for integrity
	goto EOF
)

if "%1" == "clean" (
	for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i
	del /q /s %BUILDDIR%\*
	goto EOF
)


REM Check if sphinx-build is available and fallback to Python version if any
%SPHINXBUILD% 1>NUL 2>NUL
if errorlevel 9009 goto sphinx_python
goto sphinx_ok

:sphinx_python

set SPHINXBUILD=python -m sphinx.__init__
%SPHINXBUILD% 2> nul
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

:sphinx_ok


if "%1" == "html" (
	:html
	%SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/html
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The HTML pages are in %BUILDDIR%/html.
	echo.To view, run:
	echo.  start %BUILDDIR%/html/index.html
	pause
	goto EOF
)

if "%1" == "singlehtml" (
	%SPHINXBUILD% -b singlehtml %ALLSPHINXOPTS% %BUILDDIR%/singlehtml
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The HTML pages are in %BUILDDIR%/singlehtml.
	echo.To view, run:
	echo.  start %BUILDDIR%/singlehtml/index.html
	goto EOF
)

if "%1" == "readme" (
	rst2html5.py readme.rst > build/readme.html
	echo.Build finished. The HTML page is in %BUILDDIR%/readme.html.
	echo.To view, run:
	echo.  start %BUILDDIR%/readme.html
	goto EOF
)

if "%1" == "pdf" (
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex
	cd %BUILDDIR%/latex
	make all-pdf
	cd %~dp0
	echo.
	echo.Build finished; the PDF files are in %BUILDDIR%/latex.
	goto EOF
)

if "%1" == "gettext" (
	%SPHINXBUILD% -t builder_html -b gettext %ALLSPHINXOPTS% %I18NSPHINXOPTS% %BUILDDIR%/locale
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The message catalogs are in %BUILDDIR%/locale.
	goto EOF
)

if "%1" == "epub" (
	%SPHINXBUILD% -b epub %ALLSPHINXOPTS% %BUILDDIR%/epub
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The epub file is in %BUILDDIR%/epub.
	goto EOF
)

if "%1" == "epub3" (
	%SPHINXBUILD% -b epub3 %ALLSPHINXOPTS% %BUILDDIR%/epub3
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The epub3 file is in %BUILDDIR%/epub3.
	goto EOF
)

if "%1" == "translations" (
	sphinx-intl build
	%SPHINXBUILD% -b html -D language='%2' %ALLSPHINXOPTS% %BUILDDIR%/html
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The HTML pages are in %BUILDDIR%/singlehtml.
	echo.To view, run:
	echo.  start %BUILDDIR%/html/index.html
	goto EOF
)

if "%1" == "check_links" (
    %SPHINXBUILD% -b linkcheck %ALLSPHINXOPTS% %BUILDDIR%/linkcheck
    if errorlevel 1 exit /b 1
    echo.
    echo.Link check complete; look for any errors in the above output ^
or in %BUILDDIR%/linkcheck/output.txt.
    goto end
)

if "%1" == "check_syntax" (
	python tools/rst_check_syntax.py --kbd --long > rst_check_syntax.log
	type rst_check_syntax.log
	DEL rst_check_syntax.log
	goto EOF
)

if "%1" == "update_po" (
	REM Check if SVN is in path
	where /q svn
	IF ERRORLEVEL 1 (
    	ECHO SVN is missing. Ensure it is installed and placed in your PATH.
    	GOTO EOF
	) ELSE (
    GOTO CHECK_LOCALE
	)

	REM Check if locale exists
	:CHECK_LOCALE
	IF NOT EXIST %cd%/locale GOTO MISSING_LOCALE
	cd locale

	REM Update the locale dir:
	svn cleanup .
	svn up .
	cd ../

	IF EXIST %BUILDDIR%/locale (
		REM Remove POT files:
		RMDIR /s /q %BUILDDIR%\locale
	)

	REM Create POT files:
	%SPHINXBUILD% -t builder_html -b gettext %I18NSPHINXOPTS% %BUILDDIR%/locale
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The message catalogs are in %BUILDDIR%/locale.

	REM Create PO files:
	cd manual
	sphinx-intl update -p ../%BUILDDIR%/locale
	cd ../

	cd locale
	svn --force --depth infinity add .
	cd ../

	python tools_rst/rst_check_locale.py > update_po.log
	type update_po.log
	DEL update_po.log

	echo. cd locale
	echo. svn ci -m "Update PO"
	goto EOF

	:MISSING_LOCALE
	echo. Locale directory not found... Aborting.
	goto EOF
)

if "%1" == "report_po_progress" (
	IF NOT EXIST %cd%/locale GOTO MISSING_LOCALE
	python tools_report/report_translation_progress.py locale/%2 --quiet > po_progress.log
	type po_progress.log
	DEL po_progress.log
	goto EOF

)

if "%1" == "check_structure" (
	python tools_rst/rst_check_images.py > rst_check_structure.log
	type rst_check_structure.log

	python tools_rst/rst_check_locale.py > rst_check_structure.log
	type rst_check_structure.log
	DEL rst_check_structure.log
	goto EOF

	) else (
	echo.Command not found, type make help for a list of commands. Aborting...
	goto EOF
)

:EOF
