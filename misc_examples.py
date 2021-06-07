
class SHM_window(GraphScene, MovingCameraScene):
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)

    def construct(self):
        self.amplitude = 5
        self.omega = 2
        self.camera_frame = self.camera.frame
        self.phase = np.deg2rad(0)

        title = Text("Simple Harmonic Motion")
        title.move_to(np.array([0, 0, 0]))
        title.shift(3*UP)
        fixed_point = Dot().move_to([-1*self.amplitude, 0, 0])
        fixed_point.set_color(RED)
        wall_upper_coordinates = np.array([-1*self.amplitude, 4, 0])
        wall_lower_coordinates = np.array([-1*self.amplitude, -4, 0])
        fixed_wall = Line(wall_upper_coordinates, wall_lower_coordinates, stroke_width = 2)
        moving_mass = Circle(radius = 0.2, fill_color = BLUE, opacity = 0, color = ORANGE)
        moving_mass.move_to(np.array([self.amplitude*np.sin(self.phase), 0, 0]))

        def update_mass(mob, dt):
            dtheta = self.omega*dt
            moving_mass.move_to(np.array([self.amplitude*np.sin(self.phase), 0, 0]))
            self.phase += dtheta

        def line_to_mass():
            return Line(fixed_point.get_center(), moving_mass.get_center())

        def text_redraw():
            moving_coordinates = moving_mass.get_center()
            moving_text = Text(
                "({:.2f}, {:.2f}, {:.2f})".format(moving_coordinates[0], moving_coordinates[1], moving_coordinates[2]))
            moving_text.move_to(moving_mass.get_center() + np.array([0, -0.5, 0]))
            return moving_text

        moving_text = always_redraw(text_redraw)
        spring = always_redraw(line_to_mass)
        self.add(fixed_point, fixed_wall, spring, moving_mass, title, moving_text)
        moving_mass.add_updater(update_mass)
        self.add(moving_mass, spring, moving_text)
        self.wait(10.0)
        moving_mass.remove_updater(update_mass)




class Ambient_3D(ThreeDScene):
    def construct(self):
        curve1 = ParametricFunction(
            lambda u: np.array([
                1.2 * np.cos(u),
                1.2 * np.sin(u),
                u * 0.05
            ]), color=RED, t_min=-3 * TAU, t_max=5 * TAU,
        ).set_shade_in_3d(True)
        axes = ThreeDAxes()
        self.add(axes, curve1)
        self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES)
        self.wait()

class Follow_Node_Transmission(GraphScene, MovingCameraScene):
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)
    def construct(self):
        self.camera_frame = self.camera.frame
        self.camera_frame.save_state()
        self.setup_axes(animate=False)
        graph = self.get_graph(lambda x: np.sin(x),
                               color=BLUE,
                               x_min=0,
                               x_max=3 * PI
                               )
        moving_dot = Dot().move_to(graph.points[0]).set_color(ORANGE)

        dot_at_start_graph = Dot().move_to(graph.points[0])
        dot_at_end_grap = Dot().move_to(graph.points[-1])
        self.add(graph, dot_at_end_grap, dot_at_start_graph, moving_dot)
        self.play(ApplyMethod(self.camera_frame.scale,0.5), ApplyMethod(self.camera_frame.move_to,moving_dot))

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        self.camera_frame.add_updater(update_curve)
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))
        self.camera_frame.remove_updater(update_curve)

        self.play(Restore(self.camera_frame))



class Packet_path_Creator(GraphScene, MovingCameraScene):
    def setup(self):
        GraphScene.setup(self)
        MovingCameraScene.setup(self)
        self.graph_origin = np.array([-5, 0, 0])
    def construct(self):
        self.camera_frame = self.camera.frame
        self.m = 1
        self.l = 2
        self.g = 2
        self.theta1 = np.deg2rad(20)
        self.theta2 = np.deg2rad(20)
        self.vel_theta1 = 0
        self.vel_theta2 = 0
        self.ptheta1 = (1/6)*self.m*self.l**2*(8*self.vel_theta1 + 3*self.vel_theta2*np.cos(self.theta1 - self.theta2))
        self.ptheta2 = (1/6)*self.m*self.l**2*(8*self.vel_theta2 + 3*self.vel_theta2*np.cos(self.theta1 - self.theta2))
        fixed_point = Dot().shift(1*UP)
        joint = Dot().move_to(fixed_point.get_center() + np.array([self.l*np.sin(self.theta1)
                                                           , -1*self.l*np.cos(self.theta1), 0]))
        free_end = Dot().move_to(joint.get_center() + np.array([self.l*np.sin(self.theta2), -1*self.l*np.cos(self.theta2), 0]))
        upper_rod = Line(fixed_point, joint, color = YELLOW)
        lower_rod = Line(joint, free_end, color = GREEN)
        def pt1(t1, t2, vt1, vt2):
            return (self.m*self.l**2/6)*(8*vt1 + 3*vt2*np.cos(t1 - t2))
        def pt2(t1, t2, vt1, vt2):
            return (self.m*self.l**2/6)*(2*vt2 + 3*vt1*np.cos(t1 - t2))
        def t1dot(t1, t2, vt1, vt2):
            ptheta1 = pt1(t1, t2, vt1, vt2)
            ptheta2 = pt2(t1, t2, vt1, vt2)
            return (6/(self.m*self.l**2))*(2*ptheta1 - 3*np.cos(t1 - t2)*ptheta2)/(16 - 9*(np.cos(t1 - t2))**2)
        def t2dot(t1, t2, vt1, vt2):
            ptheta1 = pt1(t1, t2, vt1, vt2)
            ptheta2 = pt2(t1, t2, vt1, vt2)
            return (6/(self.m*self.l**2))*(8*ptheta2 - 3*np.cos(t1 - t2)*ptheta1)/(16 - 9*(np.cos(t1 - t2))**2)
        def update_joint(mob, dt):
            theta1 = self.theta1
            theta2 = self.theta2
            vel_theta1 = self.vel_theta1
            vel_theta2 = self.vel_theta2
            ptheta1 = self.ptheta1
            ptheta2 = self.ptheta2
            dtheta1 = ((6/(self.m*self.l**2))*(2*ptheta1 - 3*np.cos(theta1 - theta2)*ptheta2)/(16 - 9*(np.cos(theta1 - theta2))**2))*dt
            dtheta2 = ((6/(self.m*self.l**2))*(8*ptheta2 - 3*np.cos(theta1 - theta2)*ptheta1)/(16 - 9*(np.cos(theta1 - theta2))**2))*dt
            self.theta1 += dtheta1
            self.theta2 += dtheta2
            self.vel_theta1 = t1dot(theta1, theta2, vel_theta1, vel_theta2)
            self.vel_theta2 = t2dot(theta1, theta2, vel_theta1, vel_theta2)
            dptheta1 = ((-1*self.m*self.l**2/2)*(vel_theta1*vel_theta2*np.sin(theta1 - theta2) + 3*self.g*np.sin(theta1)))*dt
            dptheta2 = ((-1*self.m*self.l**2/2)*(-1*vel_theta1*vel_theta2*np.sin(theta1 - theta2) + self.g*np.sin(theta1)))*dt
            self.ptheta1 +=dptheta1
            self.ptheta2 += dptheta2
            mob.move_to(fixed_point.get_center() + np.array([self.l * np.sin(self.theta1)
                , -1 * self.l * np.cos(self.theta1), 0]))

        def update_freeend(mob, dt):
            theta1 = self.theta1
            theta2 = self.theta2
            vel_theta1 = self.vel_theta1
            vel_theta2 = self.vel_theta2
            ptheta1 = self.ptheta1
            ptheta2 = self.ptheta2
            dtheta1 = ((6 / (self.m * self.l ** 2)) * (2 * ptheta1 - 3 * np.cos(theta1 - theta2) * ptheta2) / (
                        16 - 9 * (np.cos(theta1 - theta2)) ** 2)) * dt
            dtheta2 = ((6 / (self.m * self.l ** 2)) * (8 * ptheta2 - 3 * np.cos(theta1 - theta2) * ptheta1) / (
                        16 - 9 * (np.cos(theta1 - theta2)) ** 2)) * dt
            self.theta1 += dtheta1
            self.theta2 += dtheta2
            self.vel_theta1 = t1dot(theta1, theta2, vel_theta1, vel_theta2)
            self.vel_theta2 = t2dot(theta1, theta2, vel_theta1, vel_theta2)
            dptheta1 = ((-1 * self.m * self.l ** 2 / 2) * (
                        vel_theta1 * vel_theta2 * np.sin(theta1 - theta2) + 3 * self.g * np.sin(theta1))) * dt
            dptheta2 = ((-1 * self.m * self.l ** 2 / 2) * (
                        -1 * vel_theta1 * vel_theta2 * np.sin(theta1 - theta2) + self.g * np.sin(theta1))) * dt
            self.ptheta1 += dptheta1
            self.ptheta2 += dptheta2

            mob.move_to(joint.get_center() + np.array([self.l * np.sin(self.theta2), -1 * self.l * np.cos(self.theta2), 0]))

        def update_rod1(mob):
            mob.become(Line(fixed_point, joint, color=YELLOW))

        def update_rod2(mob):
            mob.become(Line(joint, free_end, color = GREEN))

        #self.add(fixed_point, joint, free_end, upper_rod, lower_rod)
        joint.add_updater(update_joint)
        free_end.add_updater(update_freeend)
        upper_rod.add_updater(update_rod1)
        lower_rod.add_updater(update_rod2)
        self.add(fixed_point, joint, free_end, upper_rod, lower_rod)
        print(self.theta1, self.theta2)
        self.wait(50.0)
        print(self.theta1, self.theta2)
        joint.remove_updater(update_joint)
        free_end.remove_updater(update_freeend)
        upper_rod.remove_updater(update_rod1)
        lower_rod.remove_updater(update_rod2)
