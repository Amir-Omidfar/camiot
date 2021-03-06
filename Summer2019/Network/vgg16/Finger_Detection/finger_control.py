import numpy as np
import cv2 
from matplotlib import pyplot as plt

from binary_image import binary_image_r

def finger_control_f(img_dir,thre, down_thr=30,left_thr=-9., right_thr=2.):
	img_o = cv2.imread(img_dir)
	img = binary_image_r(img_o,thre)
	
	#img = cv2.cvtColor(img_in.copy(),cv2.COLOR_BGR2GRAY)
	height,width = img.shape
	#print(width-9)
	all_ct_pt =[]
	slope = []


	white_areas=[]
	start_point = 8
	current_point = 8
	white_thr = 230
	black_thr = 10

	# get the white range for each line
	for pixel in range(4,width-4,4):
		#print((pixel,img[height-1,pixel]))
		if img[height-1,pixel] >white_thr:
			if img[height-1, pixel - 4] < black_thr :
				start_point = pixel
			elif img[height-1, pixel - 4] >white_thr or img[height-1, pixel + 4] > white_thr:
				current_point = pixel
			
			if pixel > width -9:
				current_point = pixel
				white_areas.append((start_point,current_point))
		elif img[height-1,pixel] == 0:
			if img[height-1, pixel - 4] >white_thr and start_point < current_point:
				white_areas.append((start_point,current_point))
	#print('White areas: ',white_areas)
	# if no white area, return the original image
	if white_areas ==[]:
		general_k = 1000
		to_crop_v = height
		control_signal = 'Down'
		return img, general_k, to_crop_v, control_signal
	# find the mean point of each line
	else:
		max_dif = 0
		for item in white_areas:
			if item[1] - item[0] > max_dif:
				max_dif = item[1] - item[0]
				mid_point = int(np.mean(item))
		#print(max_dif)
		# if the length of the white line exceed a upper bound, the white line is not accurate. 
		# Do the while line detection from the beginning
		if max_dif > width // 3:
			#print('Cropping!')
			img_o = img_o[:height*75//100,:]
			img = binary_image_r(img_o,thre)
	
			#img = cv2.cvtColor(img_in.copy(),cv2.COLOR_BGR2GRAY)
			height,width = img.shape
			all_ct_pt =[]
			slope = []


			white_areas=[]
			start_point = 8
			current_point = 8
			white_thr = 240
			black_thr = 10
			for pixel in range(4,width-4,4):
				#print((pixel,img[height-1,pixel]))
				if img[height-1,pixel] > white_thr:
					if img[height-1, pixel - 4] < black_thr :
						start_point = pixel
					elif img[height-1, pixel - 4] >white_thr or img[height-1, pixel + 4] > white_thr:
						current_point = pixel
					elif pixel > width -9:
						current_point = pixel
						white_areas.append((start_point,current_point))
				elif img[height-1,pixel] == 0:
					if img[height-1, pixel - 4] >white_thr and start_point < current_point:
						white_areas.append((start_point,current_point))

			max_dif = 0
			for item in white_areas:
				if item[1] - item[0] > max_dif:
					max_dif = item[1] - item[0]
					mid_point = int(np.mean(item))
		# the widest while line is set to be the bottom line
		bottom_mid = mid_point
		
		# find the top of the finger
		to_crop_v = 0
		for line in range(height-1,0,-1):
			#print('Here we are')
			if img[line,mid_point] <10:
				
				if img[max(0,line-15),mid_point] <10 and img[max(0,line-30),mid_point] <10 and img[max(0,line-15),max(0,mid_point-15)] <10\
				 and img[max(0,line-15),min(width-1,mid_point+15)] <10 and img[max(0,line-30),min(mid_point+30,width-1)] <10:
					to_crop_v = line
					to_crop_width = int(line / float(398) * 532)
					break
				else:
					continue
			# find the left and right bound of each white line
			# and find the middle point of the line
			for pixel in range(mid_point,width):
				if img[line,pixel] <10 or pixel > width-9:
					rt_most = (line,pixel)
					break
			for pixel in range(mid_point,0,-1):
				if img[line,pixel] <10 or pixel < 9:
					lf_most = (line,pixel)
					break
			#print((lf_most,rt_most))
			mid_point = int(np.mean([lf_most[1],rt_most[1]]))

			#print(lf_most[1])
			#print(rt_most[1])
			
			# record the middle point coordinates
			# also calculate the slopt from current point to the base point
			if line == height-1:
				base_pt = (line,mid_point)
				all_ct_pt.append(base_pt)
			else:
				if img[line,mid_point] > 10:
					ct_pt = (line,mid_point)
					all_ct_pt.append(ct_pt)
					if ct_pt[1] - base_pt[1] != 0:
						slope.append(float(-(ct_pt[0] - base_pt[0]))/(ct_pt[1] - base_pt[1]))
					else:
						if not slope:
							slope.append(float(-(ct_pt[0] - base_pt[0]))/1)
						
				#print(ct_pt)
			#print(base_pt)
		#print(all_ct_pt)

		# shows the middle point on the original image
		for item in all_ct_pt:
			img[item[0],item[1]] = 127
			img[item[0],item[1]+1] = 127
			img[item[0],item[1]-1] = 127
			img[item[0],item[1]+2] = 127
			img[item[0],item[1]-2] = 127

		# show the top line
		for pix in range(width):
			img[to_crop_v,pix] = 127

		#print((base_pt,ct_pt))
		#print(slope)
		# the output slope is the values for the top 5 points
		general_k = np.median(slope[-5:])


		#print (slope)
		if general_k > right_thr or general_k < left_thr or np.isnan(general_k):
			direc = 'Middle'
		elif general_k < right_thr and general_k > 0:
			direc = 'Right'
		elif general_k > left_thr:
			direc = 'Left'



	# control signal classification
	control_signal = 'Down'
	# if finger doesn't show up
	if to_crop_v > height - down_thr:
		control_signal = 'Down'
	# if have finger
	else:
		control_signal = direc



		# print('General Direction of Finger is: %s with k value: %.2f' %(direc,general_k))
	return img, general_k, to_crop_v, control_signal



if __name__ == "__main__":
	while True:
		num = input('input image number: (0 to exit) ')
		if num != '0':
			img_bk,k,top,control = finger_control(num+'image.jpg',240, 30,-3,1.5)
			print('slope is ',k,'top y value is ',top)
			print('control signal is', control)
			cv2.imshow('Binary Image', img_bk)

			cv2.waitKey(0)
			cv2.destroyAllWindows()
		else:
			break