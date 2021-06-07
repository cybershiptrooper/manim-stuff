from manimlib.imports import *
import manimlib
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
import streamlit as st
import pickle
from datetime import datetime
import argparse

colors = {
    0: YELLOW_C,
    1: ORANGE,
    2: BLUE_C,
    3: PINK,
    4: GREEN_SCREEN,
    5: BLUE_A
}

class TorLayout(MovingCameraScene):
    def setup(self):
        MovingCameraScene.setup(self)
        np.random.seed(datetime.now().second)

    def construct(self):
        circles = []
        self.num_nodes = 15
        nodes_per_col = int(self.num_nodes/3)
        for i in range(self.num_nodes):
            circle = Circle(radius = 0.2, color = GREEN, opacity = 0.7)
            if i/nodes_per_col < 1:
                circle.shift(3*LEFT)
                circle.shift((i - int(nodes_per_col/2))*DOWN)
            elif i/nodes_per_col < 2 and i/nodes_per_col >= 1:
                circle.shift(1*LEFT)
                circle.shift((i - int(3*nodes_per_col/2))*DOWN)
            else:
                circle.shift(-1*LEFT)
                circle.shift((i - int(5*nodes_per_col/2))*DOWN)
            circles.append(circle)
        client = Rectangle(fill_color = ORANGE, height = 0.5, width = 0.5)
        a, b, c = np.random.choice(15, size = 3, replace = False)
        print(a, b, c);

        client.move_to(circles[3].get_center() - np.array([2.5, 0, 0]))
        server = Rectangle(fill_color = YELLOW, height = 0.5, width = 0.5)
        server.move_to(circles[12].get_center() + np.array([3, 0, 0]))
        client_text = Text("Client")
        client_text.move_to(client.get_center() - np.array([0, 1, 0]))
        server_text = Text("Server")
        server_text.move_to(server.get_center() - np.array([0, 1, 0]))
        text = Text("Tor Layout")
        text.move_to(circles[5].get_center() + np.array([0, 1, 0]))
        node_text = Text("Node")
        node_text.move_to(circles[1].get_center() - np.array([2, -1, 0]))
        arrow_text = CurvedArrow(circles[a].get_center(), node_text.get_center() + np.array([0, -0.5, 0]), angle = -PI/2)
        arrow_1 = Arrow(circles[a].get_center(), circles[b].get_center())
        arrow_2 = Arrow(circles[b].get_center(), circles[c].get_center())
        client_arrow = Arrow(client.get_center(), circles[a].get_center(), color = RED)
        server_arrow = Arrow(circles[c].get_center(), server.get_center(), color = RED)
        self.add(VGroup(*circles), text, node_text, arrow_1, arrow_2, arrow_text, client, server, client_arrow, server_arrow, client_text, server_text)
        self.play(ShowCreation(arrow_1), ShowCreation(arrow_2))
        self.wait(5)

class TORDirectory(GraphScene):
    def setup(self):
        GraphScene.setup(self)

    def construct(self):
        monA = Rectangle(height = 0.5, width = 0.5)
        kbA =  Rectangle(height = 0.25, width = 0.5)
        directory = Rectangle(height = 4, width = 1)
        directory.move_to(2*RIGHT)
        tdir = Text("D\nI\nR\nE\nC\nT\nO\nR\nY")
        tdir.arrange(DOWN, center= True)
        tdir.scale(0.5).move_to(directory.get_center())
        monA.to_corner(LEFT)
        kbA.move_to(monA.get_center()-[0, 0.6, 0])
        tA = Text("A").scale(0.7).move_to(monA.get_center())
        self.add(monA, kbA, directory, tdir, tA)

        arrow = Arrow(monA.get_center(), directory.get_center()-[0.5, 0, 0])
        text = Text("Request relay \n flag: Guard").scale(0.7)
        center = (monA.get_center() + directory.get_center())/2
        text.move_to(center + [0, 1, 0])
        a = "185.56.80.65"
        b = "51.91.73.194"
        c = "5.39.69.166"

        self.play(ShowCreation(arrow), Write(text))
        self.wait()
        arrow2 = Arrow(directory.get_center()-[0.5, 0, 0], monA.get_center())
        text2 = Text(a + "\n" + b + "\n" + c + "\n ...").scale(0.7)
        text2.move_to(center - [0, 1.2, 0])
        self.play(Transform(arrow, arrow2))
        self.play(Transform(text, text2))
        text2 = Text("List of available Guard Relay").to_corner(DOWN+RIGHT).set_color(YELLOW_C).scale(0.7)
        arrow = CurvedArrow(text2.get_center() - [1, -0.2, 0], text.get_center()+[1.2, 0, 0])
        self.play(ShowCreation(arrow),Write(text2))
        self.wait()

class TORSetUp(GraphScene):
    ##############################################
    ##############################################
    #####LOT OF ERRORS: FIX/IGNORE BEFORE USE#####
    ##############################################
    ##############################################

    def setup(self):
        GraphScene.setup(self)
        np.random.seed(datetime.now().second)

    def construct(self):
        desc = Text("First the exit node is chosen");
        self.play(Write(
            desc.scale(0.5)
        ))
        self.wait(0.5)
        desc2 = Text(
            "based on rules like protocol to follow \n (for eg: SMTP for email)").scale(0.5)
        self.play(Transform(desc, desc2))
        self.wait()
        desc2 = Text("Now A chooses a random guard relay").arrange(
            RIGHT, center = True).scale(0.5)
        self.play(Transform( desc, desc2))
        self.wait()
        self.play(FadeOut(desc))


        monA = Rectangle(height = 0.5, width = 0.5)
        kbA =  Rectangle(height = 0.25, width = 0.5)
        text = Text("A").scale(0.7).move_to(monA.get_center())
        A = VGroup(monA, kbA, text);
        self.add(A)
        monA.to_corner(LEFT)
        kbA.move_to(monA.get_center()-[0, 0.6, 0])

        monT = []
        kbT = []

        nodes = 5

        for n in range(nodes):
            monT.append(Rectangle(height = 0.5, width = 0.5))
            kbT.append(Rectangle(height = 0.25, width = 0.5))
            monT[n].move_to(2*RIGHT+3*((2*n-nodes+1)/(nodes-1))*DOWN)
            kbT[n].move_to(monT[n].get_center()-[0, 0.6, 0])
            self.add(monT[n], kbT[n])

        guard_node = np.random.choice(nodes)

        arrow = Arrow(monA.get_center(), monT[0].get_center())
        for i in range(nodes):
            mon = monT[i]
            kb = kbT[i]
            if(guard_node == i):
                arrow2 = arrow
                arrow2.set_color(GREEN_SCREEN)
                self.play(Transform(arrow, arrow2))
                for j in range(i+1, nodes):
                    self.play(FadeOut(monT[j]), FadeOut(kbT[j]))
                break;
            else:
                arrow2 = Arrow(monA.get_center(), monT[i].get_center())
                self.play(FadeOut(monT[i]), FadeOut(kbT[i]), Transform(arrow, arrow2))
        self.wait()

        nodes = getNumNodes()
        guard = VGroup(mon, kb)
        animation =  ApplyMethod(guard.move_to, [0,0,0])
        self.play(animation, FadeOut(arrow))
        desc = Text("and finally a middle relay.").scale(0.5);
        screen_elem = VGroup(guard, A)
        self.play(
            FadeOut(screen_elem),
            Write(desc)
        )
        self.wait(0.5)

class OnionRoutingKeyIDTopology(GraphScene):
    def setup(self):
        GraphScene.setup(self)
        np.random.seed(datetime.now().second)

    def construct(self):
        monA = Rectangle(height = 0.5, width = 0.5)
        kbA =  Rectangle(height = 0.25, width = 0.5)
        self.add(monA, kbA)
        monA.to_corner(LEFT)
        kbA.move_to(monA.get_center()-[0, 0.6, 0])

        monT = []
        kbT = []

        #set up nodes
        # nodes = getNumNodes()
        nodes = 3
        for n in range(nodes):
            monT.append(Rectangle(height = 0.5, width = 0.5))
            kbT.append(Rectangle(height = 0.25, width = 0.5))
            monT[n].move_to(2*RIGHT*(n%2) + 2*LEFT*((n+1)%2) +3*((2*n-nodes+1)/(nodes-1))*DOWN)
            kbT[n].move_to(monT[n].get_center()-[0, 0.6, 0])
            self.add(monT[n], kbT[n])

        #key topology
        arrow = []
        text = []
        for i in range(nodes):
            mon = monT[i]
            arrow.append(DoubleArrow(monA.get_center(), mon.get_center()))
            text.append(Text("K{}".format(i+1)))
            text[i].move_to(arrow[i].get_center()+[0, 0.5, 0])
            self.play(ShowCreation(arrow[i]))
            self.play(Write(text[i]))
        self.wait()

        
        self.play(FadeOut(VGroup(*arrow)), FadeOut(VGroup(*text)))

        #CID topology
        arrow = DoubleArrow(monA.get_center(), monT[0].get_center())
        text = Text("CID #1").scale(0.7).move_to(arrow.get_center() + [-0.5, 0.5, 0])
        self.play(ShowCreation(arrow), Write(text))
        for i in range(nodes-1):
            monS = monT[i]
            monR = monT[i+1]
            arrow = DoubleArrow(monS.get_center(), monR.get_center())
            text = Text("CID #{}".format(i+2)).scale(0.7)
            text.move_to(arrow.get_center() 
                        + [ 0.5*( (i+1)%2 - i%2 ), 0.5, 0])
            self.play(ShowCreation(arrow), Write(text))

        self.wait()


class OnionRoutingKeyExchange(GraphScene):
    def setup(self):
        GraphScene.setup(self)
        np.random.seed(datetime.now().second)

    def construct(self):
        monA = Rectangle(height = 0.5, width = 0.5)
        kbA =  Rectangle(height = 0.25, width = 0.5)
        kbA.move_to(monA.get_center()-[0, 0.6, 0])
        textA = Text("A").scale(0.7).move_to(monA.get_center())
        A = VGroup(monA, kbA, textA);
        A.to_edge(LEFT)

        monG = Rectangle(height = 0.5, width = 0.5)
        kbG =  Rectangle(height = 0.25, width = 0.5)
        kbG.move_to(monG.get_center()-[0, 0.6, 0])
        textG = Text("R").scale(0.7).move_to(monG.get_center())
        G = VGroup(monG, kbG, textG);
        # G.move_to(A.get_center()+ 4*RIGHT)

        monR = Rectangle(height = 0.5, width = 0.5)
        kbR =  Rectangle(height = 0.25, width = 0.5)
        kbR.move_to(monR.get_center()-[0, 0.6, 0])
        textR = Text("R").scale(0.7).move_to(monR.get_center())
        R = VGroup(monR, kbR, textR); 
        R.to_edge(RIGHT)

        self.add(A, G)
        CID_AG = np.random.choice(65536)
        arrow = Arrow(monA.get_center(), monG.get_center())
        text = Text("Create cell\nHalf Key(Diffie Hellman)\nCID: {}".format(CID_AG)).scale(0.5)
        centerAG = (monA.get_center() + monG.get_center())/2
        text.move_to(centerAG + [0, 0.8, 0])
        self.play(ShowCreation(arrow), Write(text))
        self.wait()
        self.play(Write(
            Text(str(CID_AG) + "\n" + "Key: K1").scale(0.5).move_to(
                G.get_center() - [0, 1, 0]).set_color(colors[0]) ))
        arrow2 = Arrow(monG.get_center(), monA.get_center())
        text2 = Text("Half Key").scale(0.5)
        text2.move_to(centerAG + [0, -0.3, 0])
        self.play(Transform(arrow, arrow2), Transform(text, text2) )
        self.wait()

        arrow2 = Arrow(monA.get_center(), monG.get_center())
        text2 = Text("Extend cell\nHalf Key\nCID: {}".format(CID_AG)).scale(0.5)
        text2.move_to(centerAG + [0, 0.8, 0])
        self.play(Transform(text, text2), Transform(arrow, arrow2))
        self.wait()

        self.play(FadeInFrom(R, LEFT))
        CID_GR = np.random.choice(65536)
        arrowG = Arrow(monG.get_center(), monR.get_center())
        textG = Text("Create cell\nHalf Key\nCID: {}".format(CID_GR)).scale(0.5)
        centerGR = (monG.get_center() + monR.get_center())/2
        textG.move_to(centerGR + [0, 0.8, 0])
        self.play(ShowCreation(arrowG), Write(textG))
        self.wait()
        self.play(Write(
            Text(str(CID_GR) + "\n" + "Key: K2").scale(0.5).move_to(
                R.get_center() - [0, 1, 0]).set_color(colors[1]) 
            ))
        arrow2 = Arrow(monR.get_center(), monG.get_center())
        text2 = Text("Half Key").scale(0.5)
        text2.move_to(centerGR + [0, -0.3, 0])
        self.play(Transform(arrowG, arrow2), Transform(textG, text2) )
        self.wait()

        arrow2 = Arrow(monG.get_center(), monA.get_center())
        text2 = Text("Half Key").scale(0.5)
        text2.move_to(centerAG + [0, -0.3, 0])
        self.play(Transform(arrow, arrow2), Transform(text, text2) )
        self.wait()

class OnionRoutingForward(GraphScene):
    def setup(self):
        GraphScene.setup(self)
        np.random.seed(datetime.now().second)

    def construct(self):
        #get nodes
        nodes = getNumNodes()

        #setup A and server
        monA = Rectangle(height = 0.5, width = 0.5)
        kbA =  Rectangle(height = 0.25, width = 0.5)
        server = Rectangle(height = 2, width = 0.8)
        monA.to_corner(LEFT)
        kbA.move_to(monA.get_center()-[0, 0.6, 0])
        server.to_corner(RIGHT)
        textA = Text("A").scale(0.8)
        tserver = Text("server(B)").scale(0.8)
        textA.move_to(monA.get_center())
        tserver.move_to(server.get_center() - [0, 1.25, 0])
        self.add(monA, kbA, server, textA, tserver)

        #setup intermediate nodes
        monT = []
        kbT = []
        tT = []
        T = []
        for n in range(nodes):
            monT.append(Rectangle(height = 0.5, width = 0.5))
            kbT.append(Rectangle(height = 0.25, width = 0.5))
            tT.append(Text("T{}".format(n+1)).scale(0.7))
            monT[n].move_to(3*((2*n-nodes+1)/(nodes-1))*DOWN + (n%2)*RIGHT +  ((n+1)%2)*LEFT)
            kbT[n].move_to(monT[n].get_center()-[0, 0.6, 0])
            tT[n].move_to(monT[n].get_center())
            T.append(VGroup(monT[n], kbT[n], tT[n]))
            self.add(T[n])

        k = 1.8
        data = Rectangle(height = 0.3*k, width = 0.6*k)
        senderBB = Rectangle(height = 0.3*k, width = 0.3*k)
        recieverBB = Rectangle(height = 0.3*k, width = 0.3*k)
        data.move_to(monA.get_center() + [1.2*k, -0.2*k, 0])
        senderBB.move_to(data.get_center() - [0.45*k, 0, 0])
        recieverBB.move_to(data.get_center() + [0.45*k, 0, 0])
        sender = Text("A").scale(0.8)
        reciever = Text("B").scale(0.8)
        sender.move_to(senderBB.get_center())
        reciever.move_to(recieverBB.get_center())
        packet = VGroup(data, senderBB, recieverBB, sender, reciever)
        sender.set_color(YELLOW_C)
        reciever.set_color(YELLOW_C)
        self.play(
            FadeInFrom(packet, LEFT),
        )
        self.wait();
        self.play(Transform(sender, 
                    Text("T{}".format(nodes)).move_to(senderBB.get_center()).set_color(YELLOW_C).scale(0.8))
                )
        #initial encryption at A(client)
        for n in range(nodes):
            packetstr = "P{}".format(n)
            packetLabel = Text(packetstr).scale(0.8).set_color(colors[n]).move_to(data.get_center());
            packetLabel.move_to(packet.get_center())
            if(n>0):
                sreplace = Text("T{}".format(nodes - n)).move_to(senderBB.get_center()).set_color(colors[n]).scale(0.8)
                rreplace = Text("T{}".format(nodes - n + 1)).move_to(recieverBB.get_center()).set_color(colors[n]).scale(0.8)
                self.play(
                    Transform(sender, sreplace),
                    Transform(reciever, rreplace)
                )
            
            self.play(Write(packetLabel))
            self.wait()

            key = ", K{})".format(nodes - n)
            encrypt = Text("E(" + packetstr + key).scale(0.8)
            encrypt.move_to(senderBB.get_center())
            encrypt.set_color(colors[n])
            self.play(
                FadeOut(packet),
                Transform(packetLabel, encrypt)
            )
            self.wait()
            # data.set_color(colors[n])
            packet = VGroup(data, senderBB, recieverBB, sender, reciever)
            if(n == nodes -1): 
                self.play(FadeOut(packetLabel))
            else:
                self.play(
                    FadeOut(packetLabel),
                    FadeInFrom(packet, LEFT),
                )

        packetstr = "P{}".format(nodes)
        packetLabel = Text(packetstr).set_color(colors[nodes]).move_to(data.get_center()).scale(0.8)
        sender = Text("A").set_color(colors[nodes]).move_to(senderBB.get_center()).scale(0.8)
        reciever = Text("T1").set_color(colors[nodes]).move_to(recieverBB.get_center()).scale(0.8)
        packet = VGroup(data, senderBB, recieverBB, sender, reciever)

        self.play(
            FadeInFrom(packet, LEFT),
            Write(packetLabel)
        )
        self.wait()
        
        #Forward pass through circuit
        for n in range(nodes):
            if(n > 0):
                sender = Text("T{}".format(n)).move_to(senderBB.get_center()).set_color(colors[nodes - n]).scale(0.8)
                reciever = Text("T{}".format(n+1)).move_to(recieverBB.get_center()).set_color(colors[nodes - n]).scale(0.8)
                packet = VGroup(data, senderBB, recieverBB, sender, reciever)
                self.play(FadeOut(packetLabel), FadeInFrom(packet, LEFT))
                packetstr = "P{}".format(nodes - n)
                packetLabel = Text(packetstr).set_color(colors[nodes - n]).move_to(data.get_center()).scale(0.8)
                self.play(Write(packetLabel))
                arrow = Arrow(monT[n-1].get_center()-[0, 0.25, 0], 
                            monT[n].get_center() + [0, 0.25, 0])
                self.play(ShowCreation(arrow))
            else:
                arrow = Arrow(monA.get_center() + [0.25, 0.25, 0],
                         monT[0].get_center()-[0, 0.25, 0])
                self.play(ShowCreation(arrow))

            endpoint =  monT[n].get_center() - [2, 0, 0]
            packet = VGroup(data, senderBB, recieverBB, sender, reciever, packetLabel)
            animation =  ApplyMethod(packet.move_to, endpoint)
            self.play(animation)
            self.wait(0.5)

            key = ", K{})".format(n+1)
            decrypt = Text("D("+packetstr+key).scale(0.7)
            decrypt.move_to(monT[n].get_center() - [1.5, 0, 0])
            decrypt.set_color(colors[nodes - n])
            packet = VGroup(data, senderBB, recieverBB, sender, reciever)
            self.play(Transform(packetLabel, decrypt ), FadeOut(packet))

        sender = Text("T{}".format(nodes)).scale(0.8).set_color(colors[0]).move_to(senderBB.get_center())
        reciever = Text("B").scale(0.8).set_color(colors[0]).move_to(recieverBB.get_center())
        packetstr = "P0"
        packet = VGroup(data, senderBB, recieverBB, sender, reciever)
        self.play(FadeOut(packetLabel), FadeInFrom(packet, LEFT))
        packetLabel = Text(packetstr).set_color(colors[0]).move_to(data.get_center()).scale(0.8)
        self.play(Write(packetLabel))
        packet = VGroup(data, senderBB, recieverBB, sender, reciever, packetLabel)
        endpoint = monT[nodes-1].get_center() + [2, 0, 0]
        animation =  ApplyMethod(packet.move_to, endpoint)
        self.play(animation)
        endpoint = server.get_center() - [2, 0, 0]
        animation =  ApplyMethod(packet.move_to, endpoint)
        arrow = Arrow(monT[nodes-1].get_center() + [0.25, 0.25, 0], 
                        server.get_center() - [0.3, 0.8, 0])
        self.play(ShowCreation(arrow))
        caution = Text("Needs SSL/TLS security").scale(0.6).set_color(YELLOW_C).to_corner(RIGHT+UP);
        arrow2 = CurvedArrow(caution.get_center() - [1, 0.3, 0], arrow.get_center()).set_color(LIGHT_GREY)
        self.play(ShowCreation(arrow2), Write(caution))
        self.play(animation)
        self.wait(0.5)

class OnionRoutingBackward(GraphScene):
    pass

def getNumNodes():
    try:
        f = open("nodes.tmp", "r")
        try:
            return int(f.read())
        except:
            return 3
    except:
        return 3

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('nodes', type=int, default = 3)
    parser.add_argument('module', type=str, default = "TorLayout")
    args = parser.parse_args()
    f = open("nodes.tmp", "w")
    f.write(str(args.nodes))  
    f.close()
    os.system("python3 -m manim TORsims.py "+args.module)
    