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
import GafferUITest

class BookmarksTest( GafferUITest.TestCase ) :

	def test( self ) :
		
		a = Gaffer.ApplicationRoot( "testApp" )
		
		bd = GafferUI.Bookmarks.acquire( a, Gaffer.FileSystemPath, category=None )
		bc = GafferUI.Bookmarks.acquire( a, Gaffer.FileSystemPath, category="myCategory" )
		
		self.assertTrue( isinstance( bd, GafferUI.Bookmarks ) )
		self.assertTrue( isinstance( bc, GafferUI.Bookmarks ) )
		
		self.assertEqual( bd.names(), [] )
		self.assertEqual( bc.names(), [] )
		
		bd.add( "test", "/test" )
		
		self.assertEqual( bd.names(), [ "test" ] )
		self.assertEqual( bc.names(), [ "test" ] )
		
		self.assertEqual( bd.get( "test" ), "/test" )
		self.assertEqual( bc.get( "test" ), "/test" )
		
		bc.add( "c", "/c" )

		self.assertEqual( bd.names(), [ "test" ] )
		self.assertEqual( bc.names(), [ "test", "c" ] )
		
		self.assertEqual( bc.get( "c" ), "/c" )
		self.assertRaises( KeyError, bd.get, "c" )
		
		bc.remove( "c" )

		self.assertEqual( bd.names(), [ "test" ] )
		self.assertEqual( bc.names(), [ "test" ] )
		
		bc.remove( "test" )

		self.assertEqual( bd.names(), [] )
		self.assertEqual( bc.names(), [] )
	
	def testPersistence( self ) :
			
		a = Gaffer.ApplicationRoot( "testApp" )
		
		b = GafferUI.Bookmarks.acquire( a, Gaffer.FileSystemPath, category=None )
		
		b.add( "a", "/a", persistent=True )
		b.add( "b", "/b", persistent=False )
	
		self.assertEqual( b.names(), [ "a", "b" ] )
		self.assertEqual( b.names( persistent = True ), [ "a" ] )
		self.assertEqual( b.names( persistent = False ), [ "b" ] )
	
	def testOverrideDefaultCategory( self ) :
		
		a = Gaffer.ApplicationRoot( "testApp" )

		bd = GafferUI.Bookmarks.acquire( a, Gaffer.FileSystemPath, category=None )
		bc = GafferUI.Bookmarks.acquire( a, Gaffer.FileSystemPath, category="myCategory" )
	
		bd.add( "a", "/a" )
		bc.add( "a", "/aa" )
		
		self.assertEqual( bc.names(), [ "a" ] )
		self.assertEqual( bd.names(), [ "a" ] )
		
		self.assertEqual( bd.get( "a" ), "/a" )
		self.assertEqual( bc.get( "a" ), "/aa" )
	
	def testAddRecent( self ) :
	
		a = Gaffer.ApplicationRoot( "testApp" )

		b = GafferUI.Bookmarks.acquire( a, Gaffer.FileSystemPath, category=None )

		self.assertEqual( b.names(), [] )
		
		b.addRecent( "/a" )
		
		self.assertEqual( b.names(), [ "Recent/a" ] )
		
		b.addRecent( "/b" )
		b.addRecent( "/c" )

		self.assertEqual( b.names(), [ "Recent/a", "Recent/b", "Recent/c" ] )
		
		b.addRecent( "/a" )
				
		self.assertEqual( b.names(), [ "Recent/b", "Recent/c", "Recent/a" ] )
		
		b.addRecent( "/d" )
		b.addRecent( "/e" )
		b.addRecent( "/f" )
		
		self.assertEqual( b.names(), [ "Recent/b", "Recent/c", "Recent/a", "Recent/d", "Recent/e", "Recent/f" ] )

		b.addRecent( "/g" )

		self.assertEqual( b.names(), [ "Recent/c", "Recent/a", "Recent/d", "Recent/e", "Recent/f", "Recent/g" ] )
	
	def testDynamic( self ) :
	
		w = GafferUI.TextWidget( "/some/value" )
		
		a = Gaffer.ApplicationRoot( "testApp" )
		b = GafferUI.Bookmarks.acquire( a, Gaffer.FileSystemPath, category=None )

		def f( forWidget ) :
			if isinstance( forWidget, GafferUI.TextWidget ) :
				return forWidget.getText()
			else :
				return "/"
			
		b.add( "t", f )
		
		self.assertEqual( b.get( "t", w ), "/some/value" )	
		
if __name__ == "__main__":
	unittest.main()
