from gym_minigrid.minigrid import *
from gym_minigrid.register import register

class GoToDoorEnv(MiniGridEnv):
    """
    Environment in which the agent is instructed to go to a given object
    named using an English text string
    """

    def __init__(
        self,
        size=5
    ):
        super().__init__(gridSize=size, maxSteps=10*size)

        self.reward_range = (-1000, 1000)

        # Flag determining whether the wait action ends the episode
        self.waitEnds = True

    def _genGrid(self, width, height):
        assert width == height

        # Randomize the player start position and orientation
        self.startPos = self._randPos(
            1, width-1,
            1, height-1
        )
        self.startDir = self._randInt(0, 4)

        # Create a grid surrounded by walls
        grid = Grid(width, height)
        for i in range(0, width):
            grid.set(i, 0, Wall())
            grid.set(i, height-1, Wall())
        for j in range(0, height):
            grid.set(0, j, Wall())
            grid.set(width-1, j, Wall())

        # Generate the 4 doors at random positions
        doorPos = []
        doorPos.append((self._randInt(2, width-2), 0))
        doorPos.append((self._randInt(2, width-2), height-1))
        doorPos.append((0, self._randInt(2, height-2)))
        doorPos.append((width-1, self._randInt(2, height-2)))

        # Generate the door colors
        doorColors = []
        while len(doorColors) < len(doorPos):
            color = self._randElem(COLOR_NAMES)
            if color in doorColors:
                continue
            doorColors.append(color)

        # Place the doors in the grid
        for idx, pos in enumerate(doorPos):
            color = doorColors[idx]
            grid.set(*pos, Door(color))

        # Select a random target door
        doorIdx = self._randInt(0, len(doorPos))
        self.targetPos = doorPos[doorIdx]
        self.targetColor = doorColors[doorIdx]

        # Generate the mission string
        self.mission = 'go to the %s door' % self.targetColor
        #print(self.mission)

        return grid

    def _observation(self, obs):
        """
        Encode observations
        """

        obs = {
            'image': obs,
            'mission': self.mission,
            'advice' : ''
        }

        return obs

    def _reset(self):
        obs = MiniGridEnv._reset(self)
        return self._observation(obs)

    def _step(self, action):
        obs, reward, done, info = MiniGridEnv._step(self, action)

        ax, ay = self.agentPos
        tx, ty = self.targetPos

        # Don't let the agent open any of the doors
        if action == self.actions.toggle:
            done = True
            reward = -1

        # Reward waiting in front of the target door
        if action == self.actions.wait:
            if (ax == tx and abs(ay - ty) == 1) or (ay == ty and abs(ax - tx) == 1):
                reward = 1
            else:
                reward = 0
            done = self.waitEnds

        obs = self._observation(obs)

        return obs, reward, done, info

class GoToDoor8x8Env(GoToDoorEnv):
    def __init__(self):
        super().__init__(size=8)

class GoToDoor6x6Env(GoToDoorEnv):
    def __init__(self):
        super().__init__(size=6)

register(
    id='MiniGrid-GoToDoor-5x5-v0',
    entry_point='gym_minigrid.envs:GoToDoorEnv'
)

register(
    id='MiniGrid-GoToDoor-6x6-v0',
    entry_point='gym_minigrid.envs:GoToDoor6x6Env'
)

register(
    id='MiniGrid-GoToDoor-8x8-v0',
    entry_point='gym_minigrid.envs:GoToDoor8x8Env'
)