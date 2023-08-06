import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import pybullet as p
import pybullet_data
import math
import numpy as np
import random


MAX_EPISODE_LEN = 20*100

class UrgxyEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.step_counter = 0
        p.connect(p.GUI)
        p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=0, cameraPitch=-40, cameraTargetPosition=[0.55,-0.35,0.2])
        # self.action_space = spaces.Box(np.array([-1]*4), np.array([1]*4))
        #         # self.observation_space = spaces.Box(np.array([-1]*5), np.array([1]*5))
        self.action_space = spaces.Box(np.array([-1] * 3), np.array([1] * 3))
        self.observation_space = spaces.Box(np.array([-1] * 3), np.array([1] * 3))

    def step(self, action):
        p.configureDebugVisualizer(p.COV_ENABLE_SINGLE_STEP_RENDERING)
        #orientation = p.getQuaternionFromEuler([0.,-math.pi,math.pi/2.])
        dv = 0.05
        dx = action[0] * dv
        dy = action[1] * dv
        dz = action[2] * dv
        #fingers = action[3]

        currentPose = p.getLinkState(self.pandaUid,20)
        currentPosition = currentPose[0]
        orientation = p.getLinkState(self.pandaUid,20)[1]
        #currentPose = p.getLinkState(self.pandaUid, 11)

        newPosition = [currentPosition[0] + dx,
                       currentPosition[1] + dy,
                       currentPosition[2] + dz]
        #jointPoses = p.calculateInverseKinematics(self.pandaUid,20,newPosition, orientation)[0:7]
        jointPoses = p.calculateInverseKinematics(self.pandaUid, 20, newPosition, orientation)[0:12]  #得到角度
        #p.setJointMotorControlArray(self.pandaUid, list(range(12)), p.POSITION_CONTROL, list(jointPoses))
        # p.setJointMotorControl2(self.pandaUid, 15 , p.POSITION_CONTROL, jointPoses[6])
        # p.setJointMotorControl2(self.pandaUid, 16,  p.POSITION_CONTROL, jointPoses[7])
        # p.setJointMotorControl2(self.pandaUid, 17,  p.POSITION_CONTROL, jointPoses[8])
        # p.setJointMotorControl2(self.pandaUid, 18,  p.POSITION_CONTROL, jointPoses[9])
        # p.setJointMotorControl2(self.pandaUid, 19,  p.POSITION_CONTROL, jointPoses[10])
        # p.setJointMotorControl2(self.pandaUid, 20,  p.POSITION_CONTROL, jointPoses[11])
        p.setJointMotorControlArray(self.pandaUid, [15, 20], p.POSITION_CONTROL, [jointPoses[6], jointPoses[11]])
        p.stepSimulation()
        state_robot = p.getLinkState(self.pandaUid, 20)[0]  #得到位置

        done = False
        goal = np.array( [-0.8746627265025098,-0.46638541744607026,0.23835711380789043] )
        current = np.array( [state_robot[0],state_robot[1],state_robot[2]] )
        reward = -np.linalg.norm( current-goal )
        # reward = 0
        # if action[0]>0 and state_robot[0]-(-0.8746627265025098) < 0:
        #     reward += 1
        #     done = False
        #
        # if action[0]<0 and state_robot[0]-(-0.8746627265025098) > 0:
        #     reward += 1
        #     done = False
        #
        #
        # if action[1]>0 and state_robot[1]-(-0.46638541744607026) < 0:
        #     reward += 1
        #     done = False
        # # if action[1]>0 and state_robot[1]-(-0.46638541744607026) > 0:
        # #     reward -= 1
        # #     done = False
        # if action[1]<0 and state_robot[1]-(-0.46638541744607026) > 0:
        #     reward += 1
        #     done = False
        # # if action[1]<0 and state_robot[1]-(-0.46638541744607026) < 0:
        # #     reward -= 1
        # #     done = False
        #
        # if state_robot[1] > -0.2:
        #     reward -= 10000
        #     done = True
        #
        # if action[2]>0 and state_robot[2]-0.23835711380789043 < 0:
        #     reward += 1
        #     done = False
        # if action[2]>0 and state_robot[2]-0.23835711380789043 > 0:
        #     reward -= 1
        #     done = False
        # if action[2]<0 and state_robot[2]-0.23835711380789043 > 0:
        #     reward += 1
        #     done = False
        # if action[2]<0 and state_robot[2]-0.23835711380789043 < 0:
        #     reward -= 1
        #     done = False

        self.step_counter += 1

        if self.step_counter > MAX_EPISODE_LEN:
            reward = 0
            done = True

        #info = {'object_position': state_object}
        info = {'robot_position':state_robot}
        self.observation = state_robot
        return np.array(self.observation).astype(np.float32), reward, done, info

    def reset(self):
        self.step_counter = 0
        p.resetSimulation()
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0) # we will enable rendering after we loaded everything
        urdfRootPath=pybullet_data.getDataPath()
        #p.setGravity(0,0,-10)

        planeUid = p.loadURDF(os.path.join(urdfRootPath,"plane.urdf"), basePosition=[0,0,-0.65])

        #rest_poses = [0,-0.215,0,-2.57,0,2.356,2.356,0.08,0.08]
        self.pandaUid = p.loadURDF("C:/Users/guixiangyu/Desktop/artificial_potential/urdf/mobot_rl.urdf",useFixedBase=True,flags=p.URDF_USE_SELF_COLLISION)
        # for i in range(7):
        #     p.resetJointState(self.pandaUid,i, rest_poses[i])
        # p.resetJointState(self.pandaUid, 9, 0.08)
        # p.resetJointState(self.pandaUid,10, 0.08)
        rest_joints = [15.36 * 0.01745, -86.34 * 0.01745, -125.38 * 0.01745, 248.13 * 0.01745, -84.74 * 0.01745,-74.12 * 0.01745,
                       62.81 * 0.01745, -139.95 * 0.01745, 127.70 * 0.01745, -33.87 * 0.01745, 100.12 * 0.01745,30.01 * 0.01745]

        p.resetJointState(self.pandaUid, 15, rest_joints[0])
        p.resetJointState(self.pandaUid, 16, rest_joints[1])
        p.resetJointState(self.pandaUid, 17, rest_joints[2])
        p.resetJointState(self.pandaUid, 18, rest_joints[3])
        p.resetJointState(self.pandaUid, 19, rest_joints[4])
        p.resetJointState(self.pandaUid, 20, rest_joints[5])
        p.resetJointState(self.pandaUid, 1, rest_joints[6])
        p.resetJointState(self.pandaUid, 2, rest_joints[7])
        p.resetJointState(self.pandaUid, 3, rest_joints[8])
        p.resetJointState(self.pandaUid, 4, rest_joints[9])
        p.resetJointState(self.pandaUid, 5, rest_joints[10])
        p.resetJointState(self.pandaUid, 6, rest_joints[11])


        #tableUid = p.loadURDF(os.path.join(urdfRootPath, "table/table.urdf"),basePosition=[0.5,0,-0.65])
        #trayUid = p.loadURDF(os.path.join(urdfRootPath, "tray/traybox.urdf"),basePosition=[0.65,0,0])

        #state_object= [random.uniform(0.5,0.8),random.uniform(-0.2,0.2),0.05]
        #self.objectUid = p.loadURDF(os.path.join(urdfRootPath, "random_urdfs/000/000.urdf"), basePosition=state_object)
        state_robot = p.getLinkState(self.pandaUid, 20)[0]
        #state_fingers = (p.getJointState(self.pandaUid,9)[0], p.getJointState(self.pandaUid, 10)[0])
        self.observation = state_robot
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)
        return np.array(self.observation).astype(np.float32)

    def render(self, mode='human'):
        view_matrix = p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=[0.7,0,0.05],
                                                            distance=.7,
                                                            yaw=90,
                                                            pitch=-70,
                                                            roll=0,
                                                            upAxisIndex=2)
        proj_matrix = p.computeProjectionMatrixFOV(fov=60,
                                                     aspect=float(960) /720,
                                                     nearVal=0.1,
                                                     farVal=100.0)
        (_, _, px, _, _) = p.getCameraImage(width=960,
                                              height=720,
                                              viewMatrix=view_matrix,
                                              projectionMatrix=proj_matrix,
                                              renderer=p.ER_BULLET_HARDWARE_OPENGL)

        rgb_array = np.array(px, dtype=np.uint8)
        rgb_array = np.reshape(rgb_array, (720,960, 4))

        rgb_array = rgb_array[:, :, :3]
        return rgb_array

    def _get_state(self):
        return self.observation

    def close(self):
        p.disconnect()