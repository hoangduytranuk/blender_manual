# /usr/local/lib/python3.7/site-packages/sphinx/environment/__init__.py
def find_files(self, config: Config, builder: "Builder") -> None:
        """Find all source files in the source dir and put them in
        self.found_docs.
        """
        try:
            exclude_paths = (self.config.exclude_patterns +
                             self.config.templates_path +
                             builder.get_asset_paths())
            self.project.discover(exclude_paths)

            # Current implementation is applying translated messages in the reading
            # phase.Therefore, in order to apply the updated message catalog, it is
            # necessary to re-process from the reading phase. Here, if dependency
            # is set for the doc source and the mo file, it is processed again from
            # the reading phase when mo is updated. In the future, we would like to
            # move i18n process into the writing phase, and remove these lines.
            if builder.use_message_catalog:
                # add catalog mo file dependency
                repo = CatalogRepository(self.srcdir, self.config.locale_dirs,
                                         self.config.language, self.config.source_encoding)
                for docname in self.found_docs:
                    domain = docname_to_domain(docname, self.config.gettext_compact)
                    for catalog in repo.catalogs:
                        if catalog.domain == domain:
                            self.dependencies[docname].add(catalog.mo_path)
        except OSError as exc:
            raise DocumentError(__('Failed to scan documents in %s: %r') % (self.srcdir, exc))

improved:

    def find_files(self, config: Config, builder: "Builder") -> None:
        """Find all source files in the source dir and put them in
        self.found_docs.
        """
        domain_list = []
        try:
            exclude_paths = (self.config.exclude_patterns +
                             self.config.templates_path +
                             builder.get_asset_paths())
            self.project.discover(exclude_paths)

            # Current implementation is applying translated messages in the reading
            # phase.Therefore, in order to apply the updated message catalog, it is
            # necessary to re-process from the reading phase. Here, if dependency
            # is set for the doc source and the mo file, it is processed again from
            # the reading phase when mo is updated. In the future, we would like to
            # move i18n process into the writing phase, and remove these lines.
            if builder.use_message_catalog:
                # add catalog mo file dependency
                repo = CatalogRepository(self.srcdir, self.config.locale_dirs,
                                         self.config.language, self.config.source_encoding)
                logger.info(f'repo:{repo}', nonl=False)

                for docname in self.found_docs:
                    domain = docname_to_domain(docname, self.config.gettext_compact)
                    domain_list.append(domain)

                for catalog in repo.catalogs:
                    if catalog.domain in domain:
                        self.dependencies[docname].add(catalog.mo_path)
        except OSError as exc:
            raise DocumentError(__('Failed to scan documents in %s: %r') % (self.srcdir, exc))
