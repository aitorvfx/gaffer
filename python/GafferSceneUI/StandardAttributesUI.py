##########################################################################
#
#  Copyright (c) 2013, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import Gaffer
import GafferUI
import GafferScene

def __attributesSummary( plug ) :

	info = []
	if plug["visibility"]["enabled"].getValue() :
		info.append( "Visible" if plug["visibility"]["value"].getValue() else "Invisible" )
	if plug["doubleSided"]["enabled"].getValue() :
		info.append( "Double Sided" if plug["doubleSided"]["value"].getValue() else "Single Sided" )

	return ", ".join( info )

def __motionBlurSummary( plug ) :

	info = []
	for motionType in "transform", "deformation" :
		onOffEnabled = plug[motionType+"Blur"]["enabled"].getValue()
		segmentsEnabled = plug[motionType+"BlurSegments"]["enabled"].getValue()
		if onOffEnabled or segmentsEnabled :
			items = []
			if onOffEnabled :
				items.append( "On" if plug[motionType+"Blur"]["value"].getValue() else "Off" )
			if segmentsEnabled :
				items.append( "%d Segments" % plug[motionType+"BlurSegments"]["value"].getValue() )
			info.append( motionType.capitalize() + " : " + "/".join( items ) )

	return ", ".join( info )

Gaffer.Metadata.registerNode(

	GafferScene.StandardAttributes,

	"description",
	"""
	Modifies the standard attributes on objects - these should
	be respected by all renderers.
	""",

	plugs = {

		# sections

		"attributes" : [

			"layout:section:Attributes:summary", __attributesSummary,
			"layout:section:Motion Blur:summary", __motionBlurSummary,

		],

		# visibility plugs

		"attributes.visibility" : [

			"description",
			"""
			Whether or not the object can be seen - invisible objects are
			not sent to the renderer at all. Typically more fine
			grained (camera, reflection etc) visibility can be
			specified using a renderer specific attributes node.
			Note that making a parent location invisible will
			always make all the children invisible too, regardless
			of their visibility settings.
			""",

			"layout:section", "Attributes",

		],

		"attributes.doubleSided" : [

			"description",
			"""
			Whether or not the object can be seen from both sides.
			Single sided objects appear invisible when seen from
			the back.
			""",

			"layout:section", "Attributes",

		],

		# motion blur plugs

		"attributes.transformBlur" : [

			"description",
			"""
			Whether or not transformation animation on the
			object is taken into account in the rendered image.
			Use the transformBlurSegments plug to specify the number
			of segments used to represent the motion.
			""",

			"layout:section", "Motion Blur",
			"label", "Transform",

		],

		"attributes.transformBlurSegments" : [

			"description",
			"""
			The number of segments of transform animation to
			pass to the renderer when transformBlur is on.
			""",

			"layout:section", "Motion Blur",
			"label", "Transform Segments",

		],

		"attributes.deformationBlur" : [

			"description",
			"""
			Whether or not deformation animation on the
			object is taken into account in the rendered image.
			Use the deformationBlurSegments plug to specify the
			number of segments used to represent the motion.
			""",

			"layout:section", "Motion Blur",
			"label", "Deformation",

		],

		"attributes.deformationBlurSegments" : [

			"description",
			"""
			The number of segments of transform animation to
			pass to the renderer when transformBlur is on.
			""",

			"layout:section", "Motion Blur",
			"label", "Deformation Segments",

		],

		"attributes.linkedLights" : [

			"description",
			"""
			The lights to be linked to this object. Accepts a
			set expression or a space separated list of lights.
			Use __lights to refer to the set of all lights.
			""",

			"layout:section", "Light Linking",
			"label", "Linked Lights",

		],

	}

)
