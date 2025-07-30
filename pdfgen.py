# pdfgen.py
import typer
import os
import subprocess
from minio_utils import get_minio_client

app = typer.Typer()

@app.command()
def convert(bucket: str, prefix: str = ""):
    """
    Convert documents from MinIO to PDF
    """
    client = get_minio_client()
    typer.echo(f"🔍 Searching in bucket: {bucket}, folder: {prefix}")

    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    contents = response.get("Contents", [])

    if not contents:
        typer.echo("❌ No files found.")
        return

    for obj in contents:
        key = obj['Key']
        file_name = os.path.basename(key)
        typer.echo(f"📄 Found: {key}")

        # Step 1: Download to /tmp
        local_path = f"/tmp/{file_name}"
        client.download_file(bucket, key, local_path)
        typer.echo(f"⬇️ Downloaded to {local_path}")

        # Step 2: Convert to PDF
        typer.echo("🔄 Converting to PDF...")
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", "/tmp",
            local_path
        ])

        pdf_name = os.path.splitext(file_name)[0] + ".pdf"
        pdf_path = f"/tmp/{pdf_name}"
        typer.echo(f"✅ Converted: {pdf_path}")

        # Step 3 (Optional): Upload converted PDF back to MinIO
        # client.upload_file(pdf_path, bucket, f"converted/{pdf_name}")
        # typer.echo(f"☁️ Uploaded to: converted/{pdf_name}")

@app.command()
def resume():
    typer.echo("🔄 Resume not implemented yet.")

@app.command()
def status():
    typer.echo("📊 Status not implemented yet.")

if __name__ == "__main__":
    app()
