#!/usr/bin/env python
# / Image registration 3: Este me gusta mas

from __future__ import print_function

import SimpleITK as sitk
import os


def commandIteration(method):
    if method.GetOptimizerIteration() == 0:
        print("Estimated Scales: ", method.GetOptimizerScales())
    print("Iteration {0:3} = metric: {1:7.5f}, position: {2}".format(method.GetOptimizerIteration(),
                                                                     method.GetMetricValue(),
                                                                     method.GetOptimizerPosition()))


def RigidRegistration(img1, img2, type="correlation", optimizer="grad-desc", iterations=100):
    global out
    pixelType = sitk.sitkFloat32

    fixed = sitk.ReadImage(img1, sitk.sitkFloat32)
    moving = sitk.ReadImage(img2, sitk.sitkFloat32)

    R = sitk.ImageRegistrationMethod()

    if type == "correlation":
        R.SetMetricAsCorrelation()
    elif type == "mutual":
        R.SetMetricAsMattesMutualInformation(255)
    elif type == "mean-square":
        R.SetMetricAsMeanSquares()
    else:
        R.SetMetricAsMeanSquares()

    if optimizer == "grad-descent":
        R.SetOptimizerAsRegularStepGradientDescent(learningRate=0.97,
                                                   minStep=1e-4,
                                                   numberOfIterations=iterations,
                                                   gradientMagnitudeTolerance=1e-8)
    elif optimizer == "grad-step-descent":
        R.SetOptimizerAsGradientDescent(learningRate=0.9,
                                        numberOfIterations=iterations)
    else:
        R.SetOptimizerAsGradientDescent(learningRate=0.9,
                                        numberOfIterations=iterations)

    R.SetOptimizerScalesFromIndexShift()
    tx = sitk.CenteredTransformInitializer(fixed, moving, sitk.Similarity2DTransform())
    R.SetInitialTransform(tx)

    R.SetInterpolator(sitk.sitkLinear)

    R.AddCommand(sitk.sitkIterationEvent, lambda: commandIteration(R))

    outTx = R.Execute(fixed, moving)

    if not "SITK_NOSHOW" in os.environ:
        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(fixed)
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(1)
        resampler.SetTransform(outTx)

        out = resampler.Execute(moving)

    slice = sitk.GetArrayFromImage(out)
    return slice
