#!/usr/bin/env python
#/ Image registration 3: Este me gusta mas

from __future__ import print_function


import SimpleITK as sitk
import os


def command_iteration(method) :
    if (method.GetOptimizerIteration()==0):
        print("Estimated Scales: ", method.GetOptimizerScales())
    print("{0:3} = {1:7.5f} : {2}".format(method.GetOptimizerIteration(),
                                           method.GetMetricValue(),
                                           method.GetOptimizerPosition()))


def RigidRegistration(imagen1, imagen2):

    pixelType = sitk.sitkFloat32

    fixed = sitk.ReadImage(imagen1, sitk.sitkFloat32)


    moving = sitk.ReadImage(imagen2, sitk.sitkFloat32)

    R = sitk.ImageRegistrationMethod()

    R.SetMetricAsCorrelation()

    R.SetOptimizerAsRegularStepGradientDescent(learningRate=2.0,
                                           minStep=1e-4,
                                           numberOfIterations=500,
                                           gradientMagnitudeTolerance=1e-8 )
    R.SetOptimizerScalesFromIndexShift()

    tx = sitk.CenteredTransformInitializer(fixed, moving, sitk.Similarity2DTransform())
    R.SetInitialTransform(tx)

    R.SetInterpolator(sitk.sitkLinear)

    R.AddCommand( sitk.sitkIterationEvent, lambda: command_iteration(R) )

    outTx = R.Execute(fixed, moving)

    print("-------")
    print(outTx)
    print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
    print(" Iteration: {0}".format(R.GetOptimizerIteration()))
    print(" Metric value: {0}".format(R.GetMetricValue()))



    if ( not "SITK_NOSHOW" in os.environ ):

        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(fixed);
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(1)
        resampler.SetTransform(outTx)

        out = resampler.Execute(moving)

    slice = sitk.GetArrayFromImage(out)
    return slice
