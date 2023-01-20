#!/usr/bin/python3.9

# Recovers sprites (images) and sounds from a Game Maker Studio 2 project
# Tested on projects made with GMS2 v2.2.5.481

import json
import time

from pathlib import Path
from sys import platform

def nice_digits(digits,number):
	output=str(number)
	lendiff=digits-len(output)
	while lendiff>0:
		output="0"+output
		lendiff=digits-len(output)

	return output

def copy(ipath,opath):
	with open(str(ipath),"rb") as ifile:
		with open(str(opath),"wb") as ofile:
			while True:
				chunk=ifile.read(1024*1024)
				if not chunk:
					break
				if chunk:
					ofile.write(chunk)

def create_odir(opath,name):
	odir=opath.joinpath(name)
	if odir.exists():
		odir=opath.joinpath(name+"."+time.strftime("%Y-%m-%d-%H-%M-%S"))

	odir.mkdir()
	return odir

def yy_json_readfile(yy_json_file):
	json_ok={}
	json_raw=open(str(yy_json_file)).read()
	json_raw=json_raw.strip()

	try:
		json_extracted=json.loads(json_raw)
	except Exception as e:
		print("Error (1) yy_json_getfile():",e)
	else:
		json_ok=json_extracted

	if not json_ok:
		true=True
		false=False
		null=None
		undefined=None

		try:
			assert json_raw.startswith("{") and json_raw.startswith("}")
			json_extracted=eval(json_raw)
		except Exception as e:
			print("Error (2) yy_json_getfile():",e)
		else:
			json_ok=json_extracted

	return json_ok

def yy_json_getfile(fse_list,yy_dir):
	target_name=yy_dir.name+".yy"
	for fse in fse_list:
		if fse.name==target_name:
			return fse

	return None

def recover_sound(opath,fse_list,yy_data):
	# TODO: Finish code for recovering sound files
	pass

def recover_sprite(opath,fse_list,yy_data):

	if not ("frames" in yy_data):
		return

	if len(yy_data["frames"])==0:
		return

	outdir=create_odir(opath,yy_data["name"])

	recovered=0
	results={"total":len(yy_data["frames"]),"recovered":0}

	index=0
	digits=len(str(len(yy_data["frames"])))
	for frame in yy_data["frames"]:
		if "id" in frame:
			curr_id=frame["id"]
			for fse in fse_list:
				if fse.stem==curr_id:
					fse_rec_name=nice_digits(digits,index)
					fse_rec=outdir.joinpath(fse_rec_name+fse.suffix)
					if fse.exists():
						copy(fse,fse_rec)

					recovered=recovered+1
					break

			index=index+1

	results["recovered"]=recovered
	return results

# All functions below this point can be used individually

def recover(opath,yy_res_dir):

	if type(opath) is str:
		opath=Path(opath)

	opath.mkdir(parents=True,exist_ok=True)

	if type(yy_res_dir) is str:
		yy_res_dir=Path(yy_res_dir)

	fse_list=list(yy_res_dir.glob("*"))
	fse_yy_json=yy_json_getfile(fse_list,yy_res_dir)

	if not fse_yy_json:
		return

	yy_data=yy_json_readfile(fse_yy_json)
	if not yy_data:
		return

	if not ("name" in yy_data):
		return

	if not ("modelName" in yy_data):
		return

	if not (yy_data["modelName"] in ["GMSprite","GMSound"]):
		return

	if yy_data["modelName"]=="GMSprite":
		results=recover_sprite(opath,fse_list,yy_data)

	if yy_data["modelName"]=="GMSound":
		# results=recover_sound(opath,fse_list,yy_data)
		results=False

	return results
