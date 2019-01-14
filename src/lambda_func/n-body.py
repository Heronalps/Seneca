import math, random, string, boto3, datetime, os, time
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D

s3 = boto3.resource('s3')
local_repo = os.path.join(os.path.sep, "tmp")

class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y 
        self.z = z
    def toString(self):
        print ("x : {0} y : {1} z : {2}".format(self.x, self.y, self.z))
class body:
    def __init__(self, location, mass, velocity, name=""):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.name = name

def calculate_single_body_acceleration(bodies, body_index):
    G_const = 6.67408e-11 # Unit is (m3 kg-1 s-2)
    
    # The acceleration is a point based on the object location, from which the constructed vector 
    # indicates the direction and magnitude of acceleration.
    acceleration = point(0,0,0)
    
    target_body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (target_body.location.x - external_body.location.x)**2 + (target_body.location.y - external_body.location.y)**2 + (target_body.location.z - external_body.location.z)**2
            r = math.sqrt(r)
            tmp = G_const * external_body.mass / r**3
            acceleration.x += tmp * (external_body.location.x - target_body.location.x)
            acceleration.y += tmp * (external_body.location.y - target_body.location.y)
            acceleration.z += tmp * (external_body.location.z - target_body.location.z)

    return acceleration

def compute_velocity(bodies, time_step = 1):
    for body_index, target_body in enumerate(bodies):
        acceleration = calculate_single_body_acceleration(bodies, body_index)

        target_body.velocity.x += acceleration.x * time_step
        target_body.velocity.y += acceleration.y * time_step
        target_body.velocity.z += acceleration.z * time_step 

def update_location(bodies, time_step = 1):
    for target_body in bodies:
        target_body.location.x += target_body.velocity.x * time_step
        target_body.location.y += target_body.velocity.y * time_step
        target_body.location.z += target_body.velocity.z * time_step

def compute_gravity_step(bodies, time_step=1):
    compute_velocity(bodies, time_step=time_step)
    update_location(bodies, time_step=time_step)

def run_simulation(bodies, names = None, time_step = 1, number_of_steps = 10000, report_freq = 100):
    report_freq = min(time_step * 100, number_of_steps / 100)
    #create output container for each body
    body_locations_hist = []
    for current_body in bodies:
        body_locations_hist.append({"x":[], "y":[], "z":[], "name":current_body.name})
        
    for i in range(1,int(number_of_steps)):
        compute_gravity_step(bodies, time_step = 1000)            
        
        # Sampling Frequency
        if i % report_freq == 0:
            for index, body_location in enumerate(body_locations_hist):
                body_location["x"].append(bodies[index].location.x)
                body_location["y"].append(bodies[index].location.y)           
                body_location["z"].append(bodies[index].location.z)       

    return body_locations_hist

def plot_output(bodies, outfile = None):
    fig = plot.figure()
    colours = ['r','b','g','y','m','c']
    ax = fig.add_subplot(1,1,1, projection='3d')
    max_range = 0
    for current_body in bodies: 
        max_dim = max(max(current_body["x"]),max(current_body["y"]),max(current_body["z"]))
        if max_dim > max_range:
            max_range = max_dim
        ax.plot(current_body["x"], current_body["y"], current_body["z"], c = random.choice(colours), label = current_body["name"])        
    
    ax.set_xlim([-max_range,max_range])    
    ax.set_ylim([-max_range,max_range])
    ax.set_zlim([-max_range,max_range])
    ax.legend()    
    plot.savefig(outfile)

    s3.meta.client.upload_file(
        Filename = outfile,
        Bucket = 'n-body',
        Key = "orbit_{0}.png".format(str(datetime.datetime.now().time()))
    )
    
def generate_bodies(n):
    bodies = []
    for _ in range(n):
        location = generate_point(LOWER_LOC, UPPER_LOC)
        mass = random.randrange(LOWER_MASS, UPPER_MASS)
        velocity = generate_point(LOWER_VLC, UPPER_VLC)
        chars = string.ascii_uppercase + string.digits
        name = ''.join(random.choices(chars, k=n))
        bodies.append(body(location = location, mass = mass, velocity = velocity, name = name))
    return bodies

def generate_point(lower, upper):
    return point(random.randrange(lower, upper),
                random.randrange(lower, upper),
                random.randrange(lower, upper))
    
# #planet data (location (m), mass (kg), velocity (m/s)
# sun = {"location":point(0,0,0), "mass":2e30, "velocity":point(0,0,0)}
# mercury = {"location":point(0,5.7e10,0), "mass":3.285e23, "velocity":point(47000,0,0)}
# venus = {"location":point(0,1.1e11,0), "mass":4.8e24, "velocity":point(35000,0,0)}
# earth = {"location":point(0,1.5e11,0), "mass":6e24, "velocity":point(30000,0,0)}
# mars = {"location":point(0,2.2e11,0), "mass":2.4e24, "velocity":point(24000,0,0)}
# jupiter = {"location":point(0,7.7e11,0), "mass":1e28, "velocity":point(13000,0,0)}
# saturn = {"location":point(0,1.4e12,0), "mass":5.7e26, "velocity":point(9000,0,0)}
# uranus = {"location":point(0,2.8e12,0), "mass":8.7e25, "velocity":point(6835,0,0)}
# neptune = {"location":point(0,4.5e12,0), "mass":1e26, "velocity":point(5477,0,0)}
# pluto = {"location":point(0,3.7e12,0), "mass":1.3e22, "velocity":point(4748,0,0)}

# Upper and lower bounds
UPPER_LOC = 1e13
LOWER_LOC = 1e10
UPPER_MASS = 2e32
LOWER_MASS = 1e22
UPPER_VLC = 5e5
LOWER_VLC = 5e3

'''
The parameters:
    N: the number of bodies
    number_of_steps: The number of steps extrapolating orbit
'''

def lambda_handler(event, context):
    n = int(event['N'])
    number_of_steps = int(event['number_of_steps'])

# if __name__ == "__main__":
#     n = 5
#     number_of_steps = 1000

    # Create N bodies with random location, mass and velocity
    bodies = generate_bodies(n)

    # bodies = [
    #     body( location = sun["location"], mass = sun["mass"], velocity = sun["velocity"], name = "sun"),
    #     body( location = earth["location"], mass = earth["mass"], velocity = earth["velocity"], name = "earth"),
    #     body( location = mars["location"], mass = mars["mass"], velocity = mars["velocity"], name = "mars"),
    #     body( location = venus["location"], mass = venus["mass"], velocity = venus["velocity"], name = "venus"),
    # ]
    
    motions = run_simulation(bodies, number_of_steps = number_of_steps)
    
    plot_output(motions, outfile = local_repo + '/orbits.png')
    print ("Successfully upload to S3 n-body")