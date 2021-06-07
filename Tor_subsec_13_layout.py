from manimlib.imports import *
# from manim import *
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
import streamlit as st
import pickle
import selenium

class Bandwidth_Demo_Benchmark(GraphScene):
    def setup(self):
        GraphScene.setup(self)
    def construct(self):
        self.setup_axes()
        curve1 = self.get_graph(lambda x: 4 * x - x ** 2, x_min=0, x_max=4)
        curve2 = self.get_graph(lambda x: 0.8 * x ** 2 - 3 * x + 4, x_min=0, x_max=4)
        line1 = self.get_vertical_line_to_graph(2, curve1, DashedLine, color=YELLOW)
        line2 = self.get_vertical_line_to_graph(3, curve1, DashedLine, color=YELLOW)
        area1 = self.get_area(curve1, 0.3, 0.6, dx_scaling=10, area_color=BLUE)
        area2 = self.get_area(curve2, 2, 3, bounded=curve1)
        self.add(curve1, curve2, line1, line2, area1, area2)

class Network_Packet_Lighting(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        def sphere(theta, phi):
            x_coord = np.sin(theta)*np.cos(phi)
            y_coord = np.sin(theta)*np.sin(phi)
            z_coord = np.cos(theta)

            return np.array([x_coord, y_coord, z_coord])
        self.theta_light = np.deg2rad(30)
        self.theta_phi = np.deg2rad(75)
        # self.light = self.renderer.camera.light_source
        self.omega_theta = 2
        self.omega_phi = 4
        def circle(u):
            x_coord = 2*np.cos(u)
            y_coord = 2*np.sin(u)
            z_coord = 0.1*u

            return np.array([x_coord, y_coord, z_coord])
        grid = NumberPlane(x_line_frequency = 1)

        spherical_surface = ParametricSurface(sphere, u_min = 0, u_max = PI, v_min = 0, v_max = TAU)
        circular_curve = ParametricFunction(circle, t_min = 0, t_max = 4*PI, color = GREEN)
        self.set_camera_orientation(theta = -60*DEGREES, phi = 80*DEGREES)
        self.add(grid)
        self.wait(5)
        #self.add(spherical_surface, circular_curve)
        #self.wait(2)

class Chaos_simulation_AES_nbit(Scene):
    def update_ax_and_ay(self, dt):
        num1 = -self.g * (2 * self.m1 + self.m2) * np.sin(self.theta1) - self.m2 * self.g * np.sin(self.theta1 - 2 * self.theta2)
        num2 = -2 * np.sin(self.theta1 - self.theta2) * self.m2 * (self.v2 * self.v2 * self.len2 + self.v1 * self.v1 * self.len1 * np.cos(self.theta1 - self.theta2))
        denominator = 2 * self.m1 + self.m2 - self.m2 * np.cos(2 * self.theta2 - 2 * self.theta1)
        self.a1 = (num1 + num2) / (self.len1 * denominator) * dt
        num1 = self.v1 * self.v1 * self.len1 * (self.m1 + self.m2) + self.g * (self.m1 + self.m2) * np.cos(self.theta1)
        num2 = self.v2 * self.v2 * self.len2 * self.m2 * np.cos(self.theta1 - self.theta2)
        self.a2 = (2 * np.sin(self.theta1 - self.theta2) * (num1 + num2)) / (self.len2 * denominator) * dt
    def construct(self):
        CurvesAsSubmobjects
        # var of physics
        self.theta1 = 160.00 * DEGREES  # angle between normal line and the first arm
        self.theta2 = 170.0 * DEGREES  # angle between normal line and the second arm
        self.v1 = 0.0  # angular velocity of theta1
        self.v2 = 0.0  # angular velocity of theta2
        self.a1 = 0  # acceleration of theta1
        self.a2 = 0  # acceleration of theta2
        self.len1 = 1.5  # length of the first arm between the fixed node and ball1
        self.len2 = 1.5  # length of the second arm between ball1 node and ball2
        self.m1 = 6  # mass of the ball1
        self.m2 = 8  # mass of the ball2
        self.sx = 0.0  # x axis of the fixed node
        self.sy = 2.0  # y axis of the fixed node
        self.g = 300.00  # gravitational constant
        self.friction = 0.999
        # create Mobjects
        self.ball_1 = Circle().set_fill(BLUE, opacity=1).scale(0.01 * self.m1).set_color(BLUE)
        self.ball_2 = Circle().set_fill(BLUE, opacity=1).scale(0.01 * self.m2).set_color(BLUE)
        self.line1 = Line()
        self.line2 = Line()
        self.d_pendulum = Group()
        self.d_pendulum.add(self.line1, self.line2, self.ball_1, self.ball_2)
        self.old_x = -23333.3333
        self.old_y = -23333.3333
        def update(mobj, dt):
            self.theta1 += self.v1 * dt
            self.theta2 += self.v2 * dt
            self.v1 = (self.v1 + self.a1 * dt) * self.friction
            self.v2 = (self.v2 + self.a2 * dt) * self.friction
            self.update_ax_and_ay(dt)
            x1 = self.len1 * np.sin(self.theta1) + self.sx
            y1 = self.len1 * (-np.cos(self.theta1)) + self.sy
            self.line1.put_start_and_end_on((self.sx, self.sy, 0), (x1, y1, 0))
            x2 = self.len1 * np.sin(self.theta2) + x1
            y2 = self.len1 * (-np.cos(self.theta2)) + y1
            self.line2.put_start_and_end_on((x1, y1, 0), (x2, y2, 0))
            self.ball_1.move_to((x1, y1, 0))
            self.ball_2.move_to((x2, y2, 0))
            if (self.old_x > -23333 and self.old_y > -23333):
                self.add(Line((self.old_x, self.old_y, 0), (x2, y2, 0)).scale(1.01).set_opacity(0.15))
            self.old_x = x2
            self.old_y = y2
        self.d_pendulum.add_updater(update)
        self.add(self.d_pendulum)
        self.wait(60)