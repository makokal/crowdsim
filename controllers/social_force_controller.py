from controllers import Controller


class SocialForceController(Controller):
    """ Social Force Controller 
        Based on the social force model by Helbing et. al. 95
    """

    def __init__(self, agent, environment):
        """ Initialize the controller

            agent:
                The agent to control 

            environment:
                The world that the agent lives in (game)
        """
        self.agent = agent
        self.environment = environment


    def drive_single_step(self):
        pass


    def info(self):
        return 'Social Force Controller'