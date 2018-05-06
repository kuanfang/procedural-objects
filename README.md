# Procedural Object Generation

### Prepare
1. Normalize .obj mesh files:

    ```Shell
    python normalize_mesh.py --input data/example/duck_vhacd.obj --output outputs/
    ```

2. Visualize a .urdf or .obj file:

    ```Shell
    python visualize.py --input outputs/000000/body.urdf
    ```
    or
    ```Shell
    python visualize.py --input outputs/000000/head.obj
    ```

### Generation
1. Generate realistic objects:

    ```Shell
    python generate.py --body t --color realistic --mesh data/example/duck_vhacd.obj --output outputs/ --num 1
    ```
