#!/usr/bin/env python

import sys
import argparse
from sender import Sender
from rl.reinforce import Reinforce


class Trainer(object):
    def __init__(self, ip, port, algorithm):
        self.ip = ip
        self.port = port

        self.state_dim = 10
        self.action_cnt = 3
        self.max_episodes = 10
        self.max_steps = 10

        if algorithm == 'reinforce':
            self.learner = Reinforce(state_dim=self.state_dim,
                                     action_cnt=self.action_cnt)

    def run(self):
        for episode_i in xrange(1, self.max_episodes + 1):
            sender = Sender(self.ip, self.port)
            sender.init_rl_params(
                state_dim=self.state_dim,
                max_steps=self.max_steps,
                delay_weight=0.8,
                sample_action=self.learner.sample_action)

            sender.run()

            experience = sender.get_experience()
            self.learner.store_experience(experience)
            self.learner.update_model()

            sender.cleanup()

            sys.stderr.write('Episode %s\n' % episode_i)
            sys.stderr.write('Final reward: %s\n' % experience[2])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', metavar='IP')
    parser.add_argument('port', type=int)
    parser.add_argument(
        '--algorithm', choices=['reinforce'], default='reinforce',
        help='reinforcement learning algorithm to train the sender')
    args = parser.parse_args()

    trainer = Trainer(args.ip, args.port, args.algorithm)
    trainer.run()


if __name__ == '__main__':
    main()
