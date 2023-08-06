;;; Project-wide Emacs settings
;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil .
  ((mode . conda-env-autoactivate)
   (conda-project-env-path . "jupyterlab-daw_dev")
   (multi-compile-alist . (("\\.ts[x]*\\'" . (("compile typescript" . "jlpm build:lib")
                                             ("build labextension (dev)" . "jlpm build:lib && jlpm build:labextension:dev")
                                             ("build all" . "jlpm build:prod")
                                             ("clean lib" . "jlpm clean:lib")
                                             ("clean labextension" . "jlpm clean:lib")
                                             ("clean all" . "jlpm clean:all")
                                             ("test" . "jlpm test")
                                             ("test coverage" . "jlpm test-coverage")
                                             ("lint" . "jlpm lint")
                                             ("lint check" . "jlpm lint:check")))
                           (python-mode . (("lint" . "ruff check . --fix && black .")
                                           ("lint check" . "ruff check . && black --check ."))))))))
