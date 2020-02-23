#!/usr/bin/clisp
;;;; Describe program -- basic comment
#||
multi-line
;;  comment before code line
; after code line
||#
;;(format t "Hello world ~%")
(print "What's your name")

(defvar *name* (read))

(defun hello-you (*name*)
    (format t "Hello ~a! ~%" *name*)
)

(setq *print-case* :capitalize)

(Hello-you *name*)
