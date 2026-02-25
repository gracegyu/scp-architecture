<?xml version="1.0" encoding="UTF-8"?>
<Report TemplateName="RPT_BlankL" Version="5.1.0" ARCHIVETYPE="Template">
	<Paper PaperSize="A4" Orientation="Portrait">
		<Margin Top="10" Bottom="10" Left="10" Right="10"/>
	</Paper>
	<Page Number="1">
		<!-- Header Footer Item -->
		<TextBox BoxID="1" TextMacro="Date" Editable="false">
			<Position X="0%" Y="0%"/>
			<Size Width="24%" Height="2%"/>
			<Background Color="#ffffff" Opacity="0" Transparent="true"/>
			<BorderLine Color="#000000" Opacity="0" Width="1" Type="NoPen"/>
			<Text></Text>
		</TextBox>
		<TextBox BoxID="2" TextMacro="PatientInfo" Editable="false">
			<Position X="25%" Y="0%"/>
			<Size Width="50%" Height="4%"/>
			<Background Color="#ffffff" Opacity="0" Transparent="true"/>
			<BorderLine Color="#000000" Opacity="0" Width="1" Type="NoPen"/>
			<Text></Text>
		</TextBox>
		<TextBox BoxID="3" TextMacro="ClinicName" Editable="false">
			<Position X="0%" Y="88%"/>
			<Size Width="16%" Height="5%"/>
			<Background Color="#ffffff" Opacity="0" Transparent="true"/>
			<BorderLine Color="#000000" Opacity="0" Width="1" Type="NoPen"/>
			<Text></Text>
		</TextBox>
		<TextBox BoxID="4" TextMacro="WebSite" Editable="false">
			<Position X="17%" Y="88%"/>
			<Size Width="24%" Height="2%"/>
			<Background Color="#ffffff" Opacity="0" Transparent="true"/>
			<BorderLine Color="#000000" Opacity="0" Width="1" Type="NoPen"/>
			<Text></Text>
		</TextBox>
		<TextBox BoxID="5" TextMacro="PhoneNumber" Editable="false">
			<Position X="17%" Y="91%"/>
			<Size Width="24%" Height="2%"/>
			<Background Color="#ffffff" Opacity="0" Transparent="true"/>
			<BorderLine Color="#000000" Opacity="0" Width="1" Type="NoPen"/>
			<Text></Text>
		</TextBox>
		<TextBox BoxID="6" TextMacro="Address" Editable="false">
			<Position X="42%" Y="88%"/>
			<Size Width="48%" Height="5%"/>
			<Background Color="#ffffff" Opacity="0" Transparent="true"/>
			<BorderLine Color="#000000" Opacity="0" Width="1" Type="NoPen"/>
			<Text></Text>
		</TextBox>

		<ImageBox BoxID="7" ImageFitMode="BoxFit" Invert="false" ImageMacro="ClinicLogo" BoxType="Single" Source="None">
			<Position X="76%" Y="0%"/>
			<Size Width="14%" Height="4%"/>
			<Background Color="#ffffff" Opacity="0" Transparent="true"/>
			<BorderLine Color="#000000" Opacity="0" Width="1" Type="NoPen"/>
			<ImageFileNames>
				<ImageFile></ImageFile>
			</ImageFileNames>
			<CapturedImageInfo NeedToDrawInfo="false"></CapturedImageInfo>
		</ImageBox>
		<Annotations/>
	</Page>
</Report>
