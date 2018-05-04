# Procedural Object Generation

### Prepare
1. Normalize .obj mesh files:

    ```Shell
    python normalize_mesh.py --input data/example/duck_vhacd.obj --output outputs/
    ```

2. Visualize a .urdf or .obj file:

    ```Shell
    python visualize.py --input outputs/000000.obj
    ```
    or
    ```Shell
    python visualize.py --input outputs/*.urdf
    ```

### Generation
1. Generate realistic objects:

    ```Shell
    python generate_body.py --body hammer --mesh outputs/000000.obj --output outputs/ --num 1
    ```
