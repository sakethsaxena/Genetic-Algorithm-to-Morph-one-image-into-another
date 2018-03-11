from PIL import Image
import random
from operator import sub

class Environment:

    def __init__(self):
        
        self.source_image = raw_input("Enter path image to morph")
        self.target_image = raw_input("Enter path target image")
        self.population_size = 20
        # raw_input("Enter population size")

    def controller(self):
        agent_ins = Agent()
        agent_ins.sensor(self.source_image, self.target_image,self.population_size)
        result_image = agent_ins.actuator()
        result_image.show()


class Agent:

    def sensor(self, source_image, target_image, n):
        # Call agentfunc
        self.agentfunc(source_image, target_image, n)
    

    # Returns the evolved image after the number of iterations is greater than half the number of pixels of the smaller image
    def agentfunc(self, source_image, target_image, n):
        
        # open images
        source_im = Image.open(source_image)
        target_im = Image.open(target_image)
        tw,th = target_im.size
        sw, sh = source_im.size

        if tw < sw or th < sh:
            rw = tw
            rh = th
        else:
            rw = sw
            rh = sh

        # resize images
        source_im = source_im.resize((rw,rh))
        target_im = target_im.resize((rw,rh))

        
        # get pixel data
        source_im_p = list(source_im.getdata())
        target_im_p = list(target_im.getdata())
        pixel_count = 0
 
        # Create random initial population
        arbitrary_list = [x for x in source_im_p]
        random.shuffle(arbitrary_list)
        arbitrary_list = arbitrary_list[:n]
        
        while True:
           
            dist = []
            for pr,pg, pb in arbitrary_list:
                temp_list = []
                for tr,tg,tb in target_im_p:
                    temp_list.append(abs(pr-tr)+abs(tg-pg)+abs(pb-tb))
                dist.append(temp_list)

            index_vals = []
            

            # getting smallest/closest distances
            for val in dist:
                index_vals.append(val.index(min(val)))

            for idx, index in enumerate(index_vals):
                source_im_p[index] = arbitrary_list[idx]

            pixel_count +=1

            #stop after half the pixels are covered
            if pixel_count > rw*rh/2:
                break
            else:
                lss = []
                print pixel_count
                # mutate if same value encountered 
                # crossover otherwise to create new population
                for idx, valy in enumerate(arbitrary_list):
                    for idy, valx in enumerate(arbitrary_list):
                        if idx == idy:
                            idf = random.randint(0,2)
                            value = random.randint(0,255)
                            valy = list(valy)
                            valy[idf] = value
                            valy = tuple(valy)
                            temp_list.append(valy)
                        else:
                            temp_list = []
                            x = [val for val in valx]
                            r = [va for va in valy]
                            temp_list = x+r
                            random.shuffle(temp_list)            
                    lss.append(tuple(temp_list)[:3])
                    lss.append(tuple(temp_list)[3:])
                arbitrary_list = lss[:n]

        # Create new image
        self.image_out = Image.new(source_im.mode,source_im.size)
        self.image_out.putdata(source_im_p)  
        self.image_out.save('final.png')   


        

    def actuator(self):
        # return new image
        return self.image_out

x = Environment()
x.controller()