class AnimatedSprite:
    def __init__(self, spriteSheet, tbf=6):
        self.spriteSheet = spriteSheet
        self.frames = len(spriteSheet)
        self.frameCount = 1
        self.tbf = tbf    # time between frames
        self.tbfCount = 1
    
    def reset(self):
        self.frameCount = 1
        self.tbfCount = 1
    
    def get_sprite(self):
        return self.spriteSheet[self.frameCount-1]
    
    def get_spritesheet(self):
        return self.spriteSheet
    
    def update(self):
        self.tbfCount += 1
        if self.tbfCount > self.tbf:
            self.tbfCount = 1
            #
            self.frameCount += 1 
            if self.frameCount > self.frames:
                self.frameCount = 1
    
    def __len__(self):
        return self.frames
