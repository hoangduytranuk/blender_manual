
************
Introduction
************

Drivers control values of properties by means of a function.

Driver functions are added to a property and they set, or 'drive', the value of
that property according to the values of other properties,
small Python scripts and mathematical expressions.

For example, the *rotation* of Object 1 can be controlled by the *location* of Object 2.
It is then said that the *location* of Object 2 drives the *rotation* of Object 1.

Not only drivers can use the value of most properties as a direct mapping to other properties,
they can evaluate that value as part of a mathematical expression or Python script
and further modulate it with a function.

Effectively, drivers are animation :doc:`F-Curves </editors/graph_editor/fcurves/introduction>`,
vary with custom changing value, instead of varying with the current frame.


Graph View
==========

.. figure:: /images/animation_drivers_introduction_fcurve.png
   :align: right

   Driver curve in the Drivers editor.

The main area of the :doc:`Drivers editor </editors/drivers_editor>`
shows an :doc:`F-Curve </editors/graph_editor/fcurves/introduction>` that
represents the driver.

The *X axis* maps the output value of the driver. The units depend on the driver configuration.

The *Y axis* shows the value applied to the target property. The units depend on the property.

In the example image, if the driver value is 2.0 the property value will be 0.5.

The default F-curve is an identity map i.e. the value is applied to the driven
property as is outputted by the driver, unchanged. If the driver output value is 2.0,
the property will be 2.0.

The driver function can be defined manually with Bézier curve handles or
mathematically with a polynomial expression such as :math:`y = a + bx^2`.
Furthermore, the function can also be procedurally modulated with noise or cyclic repetitions.
See :doc:`Modifiers </editors/graph_editor/fcurves/modifiers>` for more details.


Driver Configuration
====================

A driver can be configured in the :doc:`Drivers panel </animation/drivers/drivers_panel>`.

A driver has zero, one, or more *variables*. Variables are the values of properties
or distances between two objects.

The driver *Type* determines how the variables are used. The type can be:

- A built-in function: for example, the sum of the variables.
- A scripted expression: a custom mathematical or Python expression that can make use of any existing variables.

This driver configuration outputs a single value which changes when the variables change.
This value is then evaluated through the driver function to produce the result
to be applied to the driven property.


Notes on Scripted Expressions
=============================

When a driver uses a Scripted expression, Blender can convert it to a native expression
if it is simple enough. This means that drivers are fast to evaluate with simple divisions or
mathematical expressions even on heavy scenes.

See :ref:`Simple Expressions <drivers-simple-expressions>`
for a comprehensive list of expressions that can be evaluated natively.

When the expression is not simple, it will be evaluated using Python.
As a consequence, the driver will be slower and there is a **security risk**
if the author of the Python code is unknown.
This is an important thing to take into consideration for heavy scenes and
when sharing files with other people.
See also: :doc:`Auto run </advanced/scripting/security>`.
