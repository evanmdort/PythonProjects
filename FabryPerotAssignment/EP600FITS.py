
#import important packages
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from skimage.feature import peak_local_max
from mpl_toolkits.axes_grid1 import make_axes_locatable

#open the data
data = fits.getdata('th_1-02-05-00.fit', ext=0)

#find coordinates of point
def pointCoordinate(data,xy):
    #initalize variable
    allVal = np.empty((2,2))
    maxVal = np.empty((2,2))
    first = 0
    maxDist = -float("inf")
    center = 0
    #step through each row in the data
    for row in range(len(data)-1):
        #find all the peaks that are greater than 3000 because anecdotally 3000 is the
        #brightness of the circle
        peaksVal = peak_local_max(data[row],threshold_abs=5000)
        peaksVal = np.insert(peaksVal, 0, row, axis = 1)#adds the additonal peak so it's in the same array

    #unneeded code that allowed me to see all peaks but is useful for giving
    #visual answers to the project question
        if peaksVal.shape == (2,2) and first == 1:#if we've hit the first peak pair then add it to the array
            allVal = np.concatenate((allVal,peaksVal),axis=0)#we look for 2,2 so we know we have a pair
            #2 ends on the cricle
        elif peaksVal.shape == (2,2) and first == 0:#else overwrite the empty array so we don't have empty values
            allVal = peaksVal
            first = 1
        
        #if it's 2x2 meaning we have 2 points (one on each edge of the circle)
        #then we can see if it's the farthest apart
        if peaksVal.shape == (2,2):
            #we check if the max distance is equal because we are using a square to 
            #approximate a circle so there are cases where the distance between two edges
            #is the same
            #what I mean is shown here where the center line is 3 blocks wide https://i.imgur.com/0Awrv.png
            #if the distance is the same we add it to a list of
            #all peaks with the same spacing to then average
            if abs(peaksVal[0][1]-peaksVal[1][1]) == maxDist:
                maxVal = np.concatenate((maxVal,peaksVal),axis=0)
                maxDist = peaksVal[0][1]-peaksVal[1][1]
            #if the new distance is greater start the array over
            elif abs(peaksVal[0][1]-peaksVal[1][1]) > maxDist:
                maxVal = peaksVal
                maxDist = peaksVal[0][1]-peaksVal[1][1]
            #average the width of pixels with the same edge distance to find
            #the approximate center pixel
    center = min(maxVal[:,0])+max(maxVal[:,0])
    center = center//2
    
    return center,allVal 

#calls function to find center coordinates

centX, allVal = pointCoordinate(data.T,1)
centY, allVal = pointCoordinate(data,0)

print(centX)
print(centY)

#change the pixel value to an area value 
#and divide it by the zero bin to get the bin value

rdp0 = 10#define size of initial bin
abin0 = rdp0**2
pixBin = []

for i in range(len(data)):
    for j in range(len(data)):
        pixToArea = (i-centY)**2+(j-centX)**2#step through each pixel and assign it an area value
        pixBin.append(pixToArea//abin0)#divide by the 0 bin and assign that as the pix bin value

binSum = [0 for i in range(max(pixBin))]#initalize a 0 array
pixelsInBin = [0 for i in range(max(pixBin))]

for i in range(len(data)):
    for j in range(len(data)):
        #step through each pixel and add it to the bin index it has based on
        #the value in the pixel bin table
        #to keep track of the number of pixels in the bin
        #I have another array that is incremented by 1 for each pixel added
        binSum[pixBin[j+256*i]-1] += data[i][j]
        pixelsInBin[pixBin[j+256*i]-1] += 1

binAvg = [0 for i in range(len(binSum))]#initialize average array

for k in range(len(binSum)):#averages the intensity per bin
    if pixelsInBin[k] != 0: 
        binAvg[k] = binSum[k]/pixelsInBin[k]
    else:#if no pixels intensity is 0 and avoids divide by zero error
        binAvg[k] = 0


#plot the data

#python's pyplot library is difficult to get perfect with aspect ratios
#I found this code from here 
#https://stackoverflow.com/questions/23270445/adding-a-colorbar-to-two-subplots-with-equal-aspect-ratios
#and modified it to fit my data so that when I added the colorbar it did not make the plots different dimensions
fig1 = plt.figure(1)

ax1 = fig1.add_subplot(1,2,1, aspect = "equal")
ax2 = fig1.add_subplot(1,2,2, aspect = "equal")

im1 = ax1.imshow(data, cmap='gray')
im2 = ax2.imshow(data, cmap='gray')

divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("right", size="5%", pad=0.05)

divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("right", size="5%", pad=0.05)

#Create and remove the colorbar for the first subplot
cbar1 = fig1.colorbar(im1, cax = cax1)
fig1.delaxes(fig1.axes[2])

#Create second colorbar
cbar2 = fig1.colorbar(im2, cax = cax2)

plt.tight_layout()
ax1.set_title('Ring')
ax2.set_title('Circle Center')
ax2.plot(centX, centY, 'r.')
ax1.set(xlabel='pixel', ylabel='pixel')
ax2.set(xlabel='pixel', ylabel='pixel')

#plot the ring sum
fig2 = plt.figure(2)
ax3 = fig2.add_subplot()
x = range(len(binAvg)//4)
plt.plot(x, binAvg[:len(x)])
ax3.set_title('Intensity per Bin r1dp={}'.format(rdp0))
ax3.set(xlabel='Bin Number', ylabel='Intensity Average per Pixel')
fig2.show()

#show all peak pairs
figAll = plt.figure(3)
ax1 = figAll.add_subplot()
ax1.imshow(data, cmap='gray')
ax1.set_title('All Peak Pairs')
ax1.plot(allVal[:,1],allVal[:,0], 'r.')
ax1.set(xlabel='pixel', ylabel='pixel')

figAll.show()

plt.show()


