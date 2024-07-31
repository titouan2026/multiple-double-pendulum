import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import shelve
import randomcolor
from alive_progress import alive_bar

rand_color = randomcolor.RandomColor()


g=9.81
l1=1
l2=1
m1=0.1
m2=0.1
Vtheta1=[0]
Vtheta2=[0]  
theta1=[2*np.pi/4]
theta2=[-2*np.pi/4]
dt=0.00001
n=1000000
N=10
variation=0.0001
interv=40 #periode of refreshing (ms)
fps=1000//interv #have to be integer (Hz)
delay=1.5 # (s)
duration=np.round(dt*n)
step=int(interv/round(dt*1000,3)) #element u need to jump for an interval (ms) step formard
MAXW=int(delay*fps)
print(step)
print(MAXW)
print(fps)






def run_animationMultiple(N):

    
    
    colors=rand_color.generate(hue="blue", count=N)
    
    X1=[]
    X2=[]
    Y1=[]
    Y2=[]
    
    with shelve.open('values') as values:
        print("reading data..")
        with alive_bar(N) as bar1:
            for i in range(N):
            
                try :
                    v=values["{}".format(i)]
                    
                except:
                    print("unknown error, maybe not enougth trajectory computed.")
                        
                Y1.append(-l1*np.cos(v[0]))
                X1.append(l1*np.sin(v[0]))
                Y2.append(Y1[i]-l2*np.cos(v[1]))
                X2.append(X1[i]+l2*np.sin(v[1]))
                bar1()
            
    anim_running = False
    
    n=len(Y1[0])
    
    def onClick(event):

        nonlocal anim_running

        if anim_running:

            ani.event_source.stop()

            anim_running = False

        else:

            ani.event_source.start()

            anim_running = True



    def animate(i):

        k=0
        for j in range(len(lines1)):

            lines_s1[j].set_data([0,X1[j][i]],[0,Y1[j][i]])

            lines1[j].set_data(X1[j][i],Y1[j][i])

            lines_s2[j].set_data([X1[j][i],X2[j][i]],[Y1[j][i],Y2[j][i]])

            lines2[j].set_data(X2[j][i],Y2[j][i])
            
            if i*dt>=delay:
                k=int(i-MAXW*step)
                maxw=MAXW
                
            else:
                maxw=i//step
                 
            for w in range(maxw):
                    
                lines3[j][MAXW-maxw+w].set_data(X2[j][w*step+k:k+(w+1)*step],Y2[j][w*step+k:k+(w+1)*step])
            
                



        return lines_s1,lines1,lines_s2,lines2,lines3



    fig = plt.figure(figsize=(12, 10))

    ax = fig.add_subplot(111)

    ax.set_aspect('equal', adjustable='box')

    lines_s1,lines1,lines_s2,lines2,lines3=[],[],[],[],[]
    

    for j in range(len(Y1)):

        line_s1, = ax.plot([],[],'-',color=colors[j],linewidth='2')

        lines_s1.append(line_s1)

        line1, = ax.plot([],[],'o',color=colors[j],markersize=5.5)

        lines1.append(line1)

        line_s2, = ax.plot([],[],'-',color=colors[j],linewidth='2')

        lines_s2.append(line_s2)

        line2, = ax.plot([],[],'o',color=colors[j],markersize=5.5)

        lines2.append(line2)
        
        lines3.append([])
        
        for l in range(MAXW):
            a=np.round(l/MAXW,4)
            line3, = ax.plot([],[],'-',color=colors[j],alpha= a,linewidth='0.8')
            
            lines3[j].append(line3)
        


    ax.set_ylim(-2.1,2.1)          #Délimite les ordonées de la figure

    ax.set_xlim(-2.1,2.1)          #Délimite les abscisses de la figure 

    ax.grid()                      #Dessine une grille, optionnel



    fig.canvas.mpl_connect('button_press_event', onClick)
    print(step,interv)
    frame=np.arange(0,len(Y1[0]),step)
    
        
    ani = animation.FuncAnimation(fig, animate, frames=frame, blit=False, interval=interv,repeat=False)
        

    # ani.save('wave1.gif', writer='imagemagick', fps=30)
    
    writergif = animation.PillowWriter(fps=fps) 
    ani.save("anim3.gif", writer=writergif)



    return None 







def run(N,DoWeDelete):
    try :

        with shelve.open('values') as values:
            keys=list(values.keys())
            for j in range(N):
                if not DoWeDelete and "{}".format(j) in keys:
                    print("already exist !")
                    continue
                else:
                    pass
                
                Vtheta1=[0]
                Vtheta2=[0]  
                theta1=[(2-j*variation)*np.pi/4]
                theta2=[-2*np.pi/4]
                
                print("doing calculation for the {}th trajectory".format(j+1))
                for i in range(n-1):
            
                    theta1.append(theta1[-1]+Vtheta1[-1]*dt)
                    theta2.append(theta2[-1]+Vtheta2[-1]*dt)
                    Vtheta1.append(Vtheta1[-1]+(-g*(2*m1+m2)*np.sin(theta1[-2])-m2*g*np.sin(theta1[-2]-2*theta2[-2])-2*np.sin(theta1[-2]-theta2[-2])*m2*(((Vtheta2[-1])**2)*l2+(Vtheta1[-1]**2)*l1*np.cos(theta1[-2]-theta2[-2])))/(l1*(2*m1+m2-m2*np.cos(2*theta1[-2]-2*theta2[-2])))*dt)
                    Vtheta2.append(Vtheta2[-1]+(2*np.sin(theta1[-2]-theta2[-2])*((Vtheta1[-2]**2)*l1*(m1+m2)+g*(m1+m2)*np.cos(theta1[-2])+(Vtheta2[-1]**2)*l2*m2*np.cos(theta1[-2]-theta2[-2])))/(l2*(2*m1+m2-m2*np.cos(2*theta1[-2]-2*theta2[-2])))*dt)
                
                values["{}".format(j)]=(theta1,theta2,Vtheta1,Vtheta2)
        pass
    except:     
        print("cant open or create the file")
        
run(N,False)
run_animationMultiple(N)





plt.tight_layout()
plt.show()