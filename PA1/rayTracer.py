#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code  # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image


class Color:
    def __init__(
        self,
        R,
        G,
        B,
    ):
        self.color = np.array([R, G, B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(
        self,
        gamma,
    ):
        inverseGamma = 1.0 / gamma
        self.color = np.power(self.color, inverseGamma)

    def toUINT8(
        self,
    ):
        return (np.clip(self.color, 0, 1) * 255).astype(np.uint8)


class Camera:
    def __init__(
        self,
        viewPoint_,
        viewDir_,
        viewUp_,
        viewProjNormal_,
        projDistance_,
        viewWidth_,
        viewHeight_,
    ):
        self.viewPoint = viewPoint_
        self.viewDir = viewDir_
        self.viewUp = viewUp_
        self.viewProjNormal = viewProjNormal_
        self.projDistance = projDistance_
        self.viewWidth = viewWidth_
        self.viewHeight = viewHeight_


class Shader:
    def __init__(
        self,
        diffuseColor_,
    ):
        self.diffuseColor = diffuseColor_


class Lambertian(Shader):
    def __init__(
        self,
        diffuseColor_,
    ):
        super().__init__(diffuseColor_)


class Phong(Shader):
    def __init__(
        self,
        diffuseColor_,
        specularColor_,
        exponent_,
    ):
        super().__init__(diffuseColor_)
        self.specularColor = specularColor_
        self.exponent = exponent_


class Sphere:
    def __init__(
        self,
        center_,
        radius_,
        shader_,
    ):
        self.center = center_
        self.radius = radius_
        self.shader = shader_


class Light:
    def __init__(
        self,
        position_,
        intensity_,
    ):
        self.position = position_
        self.intensity = intensity_


class Ray:
    def __init__(
        self,
        origin_,
        direction_,
    ):
        self.origin = origin_
        self.direction = direction_


def intersect(ray, sphere):
    p = ray.origin - sphere.center
    d = ray.direction
    a = d @ d
    b = p @ d
    c = p @ p - (sphere.radius**2)
    discriminant = (b * b) - (a * c)
    if discriminant < 0:
        return (-1.0, -1.0)
    return ((-b + np.sqrt(discriminant)) / a, (-b - np.sqrt(discriminant)) / a)


def rayTracing(ray, sphereList):
    sIdx = -1
    tMin = 12345667890

    for idx, sphere in enumerate(sphereList):
        tpd, tmd = intersect(ray, sphere)
        if tpd >= 0 and tpd < tMin:
            sIdx = idx
            tMin = tpd
        if tmd >= 0 and tmd < tMin:
            sIdx = idx
            tMin = tmd

    return sIdx, tMin


def shading(idx, t, ray, light, sphereList):
    # ray cannot reach to any figure
    if idx == -1:
        return Color(0, 0, 0)

    sphere = sphereList[idx]
    v = -ray.direction
    l = normalize((light.position - ray.origin) + (v * t))
    n = normalize((ray.origin - (v * t)) - sphere.center)
    lIdx, dump = rayTracing(Ray(light.position, -l), sphereList)

    # light cannot reach to the closest figure which found earlier
    if lIdx != idx:
        return Color(0, 0, 0)

    # both light and ray can reach to figure

    if sphere.shader.__class__.__name__ == "Lambertian":
        diffuseColor = sphere.shader.diffuseColor
        R = diffuseColor[0] * light.intensity[0] * max(0, n @ l)
        G = diffuseColor[1] * light.intensity[1] * max(0, n @ l)
        B = diffuseColor[2] * light.intensity[2] * max(0, n @ l)
    elif sphere.shader.__class__.__name__ == "Phong":
        h = normalize(v + l)
        diffuseColor = sphere.shader.diffuseColor
        specularColor = sphere.shader.specularColor
        exponent = sphere.shader.exponent
        R = (
            diffuseColor[0] * light.intensity[0] * max(0, n @ l)
            + specularColor[0] * light.intensity[0] * max(0, n @ h) ** exponent
        )

        G = (
            diffuseColor[1] * light.intensity[1] * max(0, n @ l)
            + specularColor[1] * light.intensity[1] * max(0, n @ h) ** exponent
        )
        B = (
            diffuseColor[2] * light.intensity[2] * max(0, n @ l)
            + specularColor[2] * light.intensity[2] * max(0, n @ h) ** exponent
        )

    return Color(R, G, B)


def normalize(v):
    return v / np.sqrt(v @ v)


"""
1. Calculate the ray from the "camera" through the pixel.
2. Determine which objects the ray intersects.
3. Compute a color for the closest intersection point.

Our image coordinate Y-axis is inverted.
"""


def main():

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir = np.array([0, 0, -1]).astype(np.float64)
    viewUp = np.array([0, 1, 0]).astype(np.float64)
    viewProjNormal = (
        -viewDir
    )  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth = 1.0
    viewHeight = 1.0
    projDistance = 1.0
    intensity = np.array([1, 1, 1]).astype(np.float64)  # how bright the light is.

    imgSize = np.array(root.findtext("image").split()).astype(np.int32)

    # declare components
    cam = None
    light = None
    shaderList = []
    sphereList = []

    # set camera
    for c in root.findall("camera"):
        viewPoint = np.array(c.findtext("viewPoint").split()).astype(np.float64)
        print(f"{'viewPoint':15s}: {viewPoint}")
        viewDir = np.array(c.findtext("viewDir").split()).astype(np.float64)
        print(f"{'viewDir':15s}: {viewDir}")
        viewUp = np.array(c.findtext("viewUp").split()).astype(np.float64)
        print(f"{'viewUp':15s}: {viewUp}")
        viewProjNormal = np.array(c.findtext("projNormal").split()).astype(np.float64)
        print(f"{'viewProjNormal':15s}: {viewProjNormal}")
        viewWidth = np.float64(c.findtext("viewWidth"))
        print(f"{'viewWidth':15s}: {viewWidth}")
        viewHeight = np.float64(c.findtext("viewHeight"))
        print(f"{'viewHeight':15s}: {viewHeight}")
        if c.findtext("projDistance"):
            projDistance = np.float64(c.findtext("projDistance"))
            print(f"{'projDistance':15s}: {projDistance}")
        cam = Camera(
            viewPoint,
            viewDir,
            viewUp,
            viewProjNormal,
            projDistance,
            viewWidth,
            viewHeight,
        )

    # set shader
    for c in root.findall("shader"):
        type_c = c.attrib["type"]
        print(f"{'type':15s}: {type_c}")
        name_c = c.attrib["name"]
        print(f"{'name':15s}: {name_c}")
        diffuseColor_c = np.array(c.findtext("diffuseColor").split()).astype(np.float64)
        print(f"{'diffuseColor':15s}: {diffuseColor_c}")
        if type_c == "Lambertian":
            shaderList.append(Lambertian(diffuseColor_c))
        elif type_c == "Phong":
            specularColor_c = np.array(c.findtext("specularColor").split()).astype(
                np.float64
            )
            print(f"{'specularColor':15s}: {specularColor_c}")
            exponent_c = np.float64(c.findtext("exponent"))
            print(f"{'exponent':15s}: {exponent_c}")
            shaderList.append(Phong(diffuseColor_c, specularColor_c, exponent_c))

    # set sphere
    for idx, c in enumerate(root.findall("surface")):
        center = np.array(c.findtext("center").split()).astype(np.float64)
        radius = np.float64(c.findtext("radius"))
        sphereList.append(Sphere(center, radius, shaderList[idx]))

    # set light
    for c in root.findall("light"):
        lightPosition = np.array(c.findtext("position").split()).astype(np.float64)
        lightIntensity = np.array(c.findtext("intensity").split()).astype(np.float64)
        light = Light(lightPosition, lightIntensity)

    # Create an empty image
    channels = 3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:, :] = 0

    # 3 unit basis vector for camera coordinate system
    w = normalize(cam.viewProjNormal)
    u = normalize(np.cross(cam.viewUp, w))
    v = normalize(np.cross(w, u))

    #  Mapping viewport to image pixel
    viewU = cam.viewWidth * u
    viewV = cam.viewHeight * -v
    pixelDeltaU = viewU / imgSize[0]
    pixelDeltaV = viewV / imgSize[1]
    viewUpperLeft = cam.viewPoint - (cam.projDistance * w) - (viewU / 2) - (viewV / 2)
    pixel00 = viewUpperLeft + 0.5 * (pixelDeltaU + pixelDeltaV)

    #  Do ray tracing and shading
    for j in np.arange(imgSize[1]):
        for i in np.arange(imgSize[0]):
            pixelCenter = pixel00 + (i * pixelDeltaU) + (j * pixelDeltaV)
            ray = Ray(cam.viewPoint, normalize(pixelCenter - cam.viewPoint))
            sIdx, tMin = rayTracing(ray, sphereList)
            pixelColor = shading(sIdx, tMin, ray, light, sphereList)
            pixelColor.gammaCorrect(2.2)
            img[j][i][:] = pixelColor.toUINT8()

    # save img
    rawimg = Image.fromarray(img, "RGB")
    rawimg.save(sys.argv[1] + ".png")


if __name__ == "__main__":
    main()
