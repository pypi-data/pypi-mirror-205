import rover_arm.keyboard_control as kc

import rover_arm.envs.roverarm_env as roverarm_env
import gym
# env = gym.make('rover-arm-pick-v0', render_mode = 'human')
env = roverarm_env.RoverArmEnv(render_mode = 'human')

keyboard_controller = kc.KeyboardAction()
keyboard_controller.start_listening()

observation = env.reset()
done = False
import time
cnt = 0
st = time.time()
while not done:
    action = keyboard_controller.action
    observation, reward, terminated, truncated, info = env.step(action)
    env.render(224, 224)
    cnt += 1
    # if cnt % 10 == 0:
    #     print(cnt, time.time() - st)
    # print(reward)
    print(action, observation, terminated, truncated, reward)
    # time.sleep(0.00001)
    x, y, z = observation[2], observation[3], observation[4]
    xo, yo, zo = info['object_position']
    # print(xo, yo , x, y , z, x - xo , y - yo, -int(((x - xo)**2 + (y - yo)**2)))
    # print(x, y , z)
    done = terminated or truncated
env.close()
# print(reward, done, info)
